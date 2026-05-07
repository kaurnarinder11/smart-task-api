from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import Optional
from app.core.logger import get_logger

logger = get_logger("storage")

class StorageBackend(ABC):
    """Abstract base class for all storage backends"""
    
    @abstractmethod
    def save(self, path: str, content: str) -> str:
        """Save content to storage, return accessible path/URL"""
        pass
    
    @abstractmethod
    def read(self, path: str) -> Optional[str]:
        """Read content from storage"""
        pass
    
    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if file exists in storage"""
        pass

class LocalStorage(StorageBackend):
    """Save files to local disk (development)"""
    
    def save(self, path: str, content: str) -> str:
        # Ensure directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"Saved locally: {path}")
        return path
    
    def read(self, path: str) -> Optional[str]:
        if not self.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    
    def exists(self, path: str) -> bool:
        return os.path.exists(path)

class S3Storage(StorageBackend):
    """Save files to AWS S3 (production)"""
    
    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        try:
            import boto3
            self.boto3 = boto3
            self.s3 = boto3.client('s3', region_name=region)
            self.bucket = bucket_name
            self.region = region
            logger.info(f"S3 Storage initialized: bucket={bucket_name}, region={region}")
        except ImportError:
            raise ImportError("boto3 is required for S3 storage. Install with: pip install boto3")
    
    def save(self, path: str, content: str) -> str:
        try:
            self.s3.put_object(
                Bucket=self.bucket, 
                Key=path, 
                Body=content.encode('utf-8'),
                ContentType='text/plain'
            )
            url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{path}"
            logger.info(f"Saved to S3: {path}")
            return url
        except Exception as e:
            logger.error(f"Failed to save to S3: {e}")
            raise
    
    def read(self, path: str) -> Optional[str]:
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=path)
            return response['Body'].read().decode('utf-8')
        except self.boto3.exceptions.botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            raise
    
    def exists(self, path: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket, Key=path)
            return True
        except self.boto3.exceptions.botocore.exceptions.ClientError:
            return False

def get_storage() -> StorageBackend:
    """Factory function that returns appropriate storage backend"""
    from app.core.config import settings
    
    # Check if S3 is configured (bucket name exists AND environment is production)
    if settings.S3_BUCKET_NAME and settings.ENVIRONMENT == "production":
        return S3Storage(
            bucket_name=settings.S3_BUCKET_NAME,
            region=settings.S3_REGION
        )
    else:
        logger.info("Using LocalStorage (S3 not configured or not in production)")
        return LocalStorage()