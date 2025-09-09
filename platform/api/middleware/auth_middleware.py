"""
Authentication middleware for the Multi-Agent Infrastructure Intelligence Platform API.

This module provides authentication and authorization functionality.
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.api_key import APIKeyHeader
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
import os

# Security schemes
security = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# JWT settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# API Key settings
API_KEYS = {
    "admin": "admin-api-key-12345",
    "user": "user-api-key-67890",
    "readonly": "readonly-api-key-abcdef"
}

# User roles and permissions
USER_ROLES = {
    "admin": ["read", "write", "delete", "admin"],
    "user": ["read", "write"],
    "readonly": ["read"]
}

# Mock user database (in production, this would be a real database)
USERS_DB = {
    "admin": {
        "user_id": "admin",
        "username": "admin",
        "email": "admin@example.com",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
        "active": True,
        "created_at": datetime.now(),
        "last_login": None
    },
    "user": {
        "user_id": "user",
        "username": "user",
        "email": "user@example.com",
        "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user",
        "active": True,
        "created_at": datetime.now(),
        "last_login": None
    }
}


class AuthenticationError(Exception):
    """Authentication error exception."""
    pass


class AuthorizationError(Exception):
    """Authorization error exception."""
    pass


def create_access_token(user_id: str, role: str) -> str:
    """Create a JWT access token."""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_access_token(token: str) -> Dict[str, Any]:
    """Verify and decode a JWT access token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == password_hash


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user with username and password."""
    if username not in USERS_DB:
        return None
    
    user = USERS_DB[username]
    if not user["active"]:
        return None
    
    if not verify_password(password, user["password_hash"]):
        return None
    
    # Update last login
    user["last_login"] = datetime.now()
    
    return user


def authenticate_api_key(api_key: str) -> Optional[str]:
    """Authenticate using API key."""
    for role, key in API_KEYS.items():
        if key == api_key:
            return role
    return None


def check_permission(user_role: str, required_permission: str) -> bool:
    """Check if a user role has the required permission."""
    if user_role not in USER_ROLES:
        return False
    
    user_permissions = USER_ROLES[user_role]
    return required_permission in user_permissions


async def get_current_user_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from JWT token."""
    try:
        token = credentials.credentials
        payload = verify_access_token(token)
        user_id = payload.get("user_id")
        role = payload.get("role")
        
        if user_id not in USERS_DB:
            raise AuthenticationError("User not found")
        
        user = USERS_DB[user_id]
        if not user["active"]:
            raise AuthenticationError("User account is inactive")
        
        return {
            "user_id": user_id,
            "username": user["username"],
            "email": user["email"],
            "role": role,
            "permissions": USER_ROLES.get(role, [])
        }
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_api_key(api_key: str = Depends(api_key_header)) -> Dict[str, Any]:
    """Get current user from API key."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    role = authenticate_api_key(api_key)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return {
        "user_id": f"api_user_{role}",
        "username": f"api_{role}",
        "email": f"{role}@api.example.com",
        "role": role,
        "permissions": USER_ROLES.get(role, [])
    }


async def get_current_user(
    jwt_user: Optional[Dict[str, Any]] = Depends(get_current_user_jwt),
    api_user: Optional[Dict[str, Any]] = Depends(get_current_user_api_key)
) -> Dict[str, Any]:
    """Get current user from either JWT or API key."""
    if jwt_user:
        return jwt_user
    elif api_user:
        return api_user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer or ApiKey"},
        )


def require_permission(permission: str):
    """Decorator to require a specific permission."""
    def permission_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if not check_permission(current_user["role"], permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    return permission_checker


def require_role(role: str):
    """Decorator to require a specific role."""
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if current_user["role"] != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' required"
            )
        return current_user
    return role_checker


def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require admin role."""
    return require_role("admin")(current_user)


def require_write_permission(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require write permission."""
    return require_permission("write")(current_user)


def require_read_permission(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require read permission."""
    return require_permission("read")(current_user)


class RateLimiter:
    """Simple rate limiter for API endpoints."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if a user is allowed to make a request."""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[user_id].append(now)
        return True


# Global rate limiter
rate_limiter = RateLimiter(max_requests=1000, window_seconds=3600)  # 1000 requests per hour


def check_rate_limit(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Check rate limit for current user."""
    if not rate_limiter.is_allowed(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    return current_user


# Authentication endpoints
from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/login")
async def login(username: str, password: str):
    """Login endpoint to get JWT token."""
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    access_token = create_access_token(user["user_id"], user["role"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user["user_id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }


@auth_router.post("/refresh")
async def refresh_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Refresh JWT token."""
    new_token = create_access_token(current_user["user_id"], current_user["role"])
    
    return {
        "access_token": new_token,
        "token_type": "bearer"
    }


@auth_router.get("/me")
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information."""
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "role": current_user["role"],
        "permissions": current_user["permissions"]
    }


@auth_router.post("/logout")
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Logout endpoint (client should discard token)."""
    return {"message": "Successfully logged out"}


@auth_router.get("/api-keys")
async def list_api_keys(current_user: Dict[str, Any] = Depends(require_admin)):
    """List available API keys (admin only)."""
    return {
        "api_keys": [
            {
                "role": role,
                "key": key[:8] + "..." + key[-4:],  # Masked key
                "permissions": USER_ROLES.get(role, [])
            }
            for role, key in API_KEYS.items()
        ]
    }
