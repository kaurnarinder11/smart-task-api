from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test 1: Normal password
print("TEST 1: Normal password")
password = "mypassword123"
hashed = pwd_context.hash(password)
print(f"Password: {password}")
print(f"Hash: {hashed}")
print(f"Verify: {pwd_context.verify(password, hashed)}")
print()

# Test 2: Password with truncation
print("TEST 2: Long password with truncation")
long_password = "x" * 100
print(f"Original length: {len(long_password)} chars")
password_bytes = long_password.encode('utf-8')[:72]
hashed2 = pwd_context.hash(password_bytes)
print(f"Truncated length: {len(password_bytes)} bytes")
print(f"Hash: {hashed2[:50]}...")
print(f"Verify: {pwd_context.verify(password_bytes, hashed2)}")
print()

# Test 3: Your actual test password
print("TEST 3: Your actual test password")
test_pass = "mypassword123"
hashed3 = pwd_context.hash(test_pass.encode('utf-8')[:72])
print(f"Works: {hashed3[:50]}...")