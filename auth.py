import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlmodel import Session, select
import hashlib
import bcrypt
from database import get_session
from models import User, TokenData


load_dotenv()

# password hashing

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30"))
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not set")

# Create a context using bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _pre_hash_password(plain_password: str) -> bytes:
    """Safely combine password with secret and shrink to 32 bytes."""
    combined = plain_password + SECRET_KEY
    return hashlib.sha256(combined.encode('utf-8')).digest()

def hash_password(plain_password: str) -> str:
    """Hash a plain text password during registration."""
    processed_bytes = _pre_hash_password(plain_password)
    
    # Generate a salt and hash the processed bytes
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(processed_bytes, salt)
    
    # Decode to string for easy database storage
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain password against its hash during login."""
    processed_bytes = _pre_hash_password(plain_password)
    
    # Verify using bcrypt's native verification engine
    return bcrypt.checkpw(processed_bytes, hashed_password.encode('utf-8'))


# token creation
def create_access_token(data: dict) -> str:
    """Create a signed JWT token containing the given claims."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Tells FastAPI where clients send tokens (the login URL)
# Also adds a padlock icon and Authorize button in /docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(token: str = Depends(oauth2_scheme),session: Session = Depends(get_session),) -> User:
    """Dependency: decodes the JWT and returns the current user."""
    credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user