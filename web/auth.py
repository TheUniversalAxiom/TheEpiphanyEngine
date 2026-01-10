"""
Authentication module for Epiphany Engine API.

Provides optional API key and JWT-based authentication.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Configuration from environment variables
API_KEY_ENABLED = os.getenv("API_KEY_ENABLED", "false").lower() == "true"
API_KEY = os.getenv("API_KEY", "")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))

# Validate configuration at module load
if API_KEY_ENABLED and not API_KEY:
    raise ValueError(
        "API_KEY_ENABLED is true but API_KEY is not set. "
        "Please set the API_KEY environment variable."
    )

if API_KEY_ENABLED and not JWT_SECRET_KEY:
    raise ValueError(
        "API_KEY_ENABLED is true but JWT_SECRET_KEY is not set. "
        "Please set JWT_SECRET_KEY to a secure random value (minimum 32 characters)."
    )

if JWT_SECRET_KEY and len(JWT_SECRET_KEY) < 32:
    raise ValueError(
        "JWT_SECRET_KEY must be at least 32 characters long for security. "
        "Please use a cryptographically secure random string."
    )

# Security schemes
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """JWT token payload data."""
    username: Optional[str] = None
    scopes: List[str] = []


class AuthConfig:
    """Centralized authentication configuration."""

    @staticmethod
    def is_enabled() -> bool:
        """Check if authentication is enabled."""
        return API_KEY_ENABLED

    @staticmethod
    def get_api_key() -> str:
        """Get the configured API key."""
        return API_KEY


def verify_api_key(api_key: str = Security(api_key_header)) -> bool:
    """
    Verify API key from request header.

    Args:
        api_key: API key from X-API-Key header

    Returns:
        True if valid

    Raises:
        HTTPException: If authentication is enabled and key is invalid
    """
    if not AuthConfig.is_enabled():
        return True  # Authentication disabled, allow all requests

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Provide X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key != AuthConfig.get_api_key():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return True


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.

    Args:
        data: Payload to encode
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> TokenData:
    """
    Verify JWT token from Authorization header.

    Args:
        credentials: Bearer token credentials

    Returns:
        Token data if valid

    Raises:
        HTTPException: If token is invalid or expired
    """
    if not AuthConfig.is_enabled():
        return TokenData()  # Authentication disabled

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return TokenData(username=username, scopes=payload.get("scopes", []))

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)
