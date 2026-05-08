"""
Safe External API Request Utility
What: Makes API calls to external services with proper error handling
Why: External APIs fail ALL the time - you need to handle:
     - Timeout (API takes too long)
     - No internet connection
     - Bad response (500, 404 from external API)
     - Network errors

Usage:
    result = safe_external_request("https://api.example.com/data")
    if result:
        # Use the data
"""

import logging
import requests
from fastapi import HTTPException
from typing import Optional, Dict, Any, Union

logger = logging.getLogger(__name__)

def safe_external_request(
    url: str,
    method: str = "GET",
    timeout: int = 5,
    retries: int = 2,
    **kwargs
) -> Optional[Union[Dict[str, Any], list]]:
    """
    Make an external API request with automatic retry and timeout
    
    Args:
        url: The API endpoint URL
        method: HTTP method (GET, POST, PUT, DELETE)
        timeout: Seconds to wait before giving up (default: 5)
        retries: How many times to retry on failure (default: 2)
        **kwargs: Additional requests params (headers, json, data, etc)
    
    Returns:
        JSON response as dict or list, or None if failed after all retries
    
    Raises:
        HTTPException: After all retries are exhausted with specific status codes
    
    Examples:
        # GET request
        data = safe_external_request("https://api.jokes.com/random")
        
        # POST with headers
        data = safe_external_request(
            "https://api.example.com/create",
            method="POST",
            headers={"Authorization": "Bearer token"},
            json={"name": "test"}
        )
    """
    
    for attempt in range(retries + 1):  # +1 because starting from 0
        try:
            logger.info(
                f"External request attempt {attempt + 1}/{retries + 1} | "
                f"Method: {method} | URL: {url}"
            )
            
            # Make the actual request with timeout
            response = requests.request(
                method=method,
                url=url,
                timeout=timeout,
                **kwargs
            )
            
            # Raise exception for bad status codes (4xx, 5xx)
            response.raise_for_status()
            
            logger.info(f"External request SUCCESS | Status: {response.status_code} | URL: {url}")
            
            # Try to parse JSON, return raw text if fails
            try:
                return response.json()
            except ValueError:
                logger.warning(f"Response not JSON, returning text: {url}")
                return {"data": response.text}
            
        except requests.exceptions.Timeout:
            logger.warning(
                f"Timeout on attempt {attempt + 1} | URL: {url} | "
                f"Timeout limit: {timeout}s"
            )
            if attempt == retries:
                raise HTTPException(
                    status_code=504,  # Gateway Timeout
                    detail=f"External service timeout after {timeout} seconds. Please try again later."
                )
                
        except requests.exceptions.ConnectionError:
            logger.warning(
                f"Connection error on attempt {attempt + 1} | URL: {url} | "
                f"Check your internet connection"
            )
            if attempt == retries:
                raise HTTPException(
                    status_code=503,  # Service Unavailable
                    detail="Cannot connect to external service. Please check your internet connection."
                )
                
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"HTTP error from external service | URL: {url} | "
                f"Status: {e.response.status_code} | Response: {e.response.text[:200]}"
            )
            # Don't retry on client errors (4xx) - they won't succeed on retry
            if 400 <= e.response.status_code < 500:
                raise HTTPException(
                    status_code=502,  # Bad Gateway
                    detail=f"External service returned client error: {e.response.status_code}"
                )
            # Retry on server errors (5xx) - might work on next attempt
            elif attempt == retries:
                raise HTTPException(
                    status_code=502,
                    detail=f"External service returned server error: {e.response.status_code}"
                )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception on attempt {attempt + 1}: {type(e).__name__} - {str(e)}")
            if attempt == retries:
                raise HTTPException(
                    status_code=500,
                    detail=f"External request failed: {str(e)[:100]}"
                )
            
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__} - {str(e)}", exc_info=True)
            if attempt == retries:
                raise HTTPException(
                    status_code=500,
                    detail="Unexpected error while calling external service"
                )
    
    return None  # Should never reach here