"""
Authentication and authorization utilities for ContentFlow AI API.
Implements JWT-based authentication and role-based access control.
"""
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from jose import jwt, JWTError
from pydantic import BaseModel
import os

SECRET_KEY = os.environ.get("CFLOW_JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    role: str

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Decode JWT and return the current user.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role", "user")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token.")
        return User(username=username, role=role)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token.")

def require_role(role: str):
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient privileges.")
        return user
    return role_dependency
