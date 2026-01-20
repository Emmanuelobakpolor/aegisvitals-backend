from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import SECRET_KEY
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def hash_password(password: str) -> str:
    """Hash password with SHA-256 pre-hashing to avoid bcrypt's 72-byte limit."""
    # First hash with SHA-256 to avoid bcrypt's length limit
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(sha256_hash)

def verify_password(password: str, hashed: str) -> bool:
    """Verify password with SHA-256 pre-hashing."""
    # Hash the plain password with SHA-256 first
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.verify(sha256_hash, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)