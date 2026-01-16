from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.user import UserRole


class UserCreate(BaseModel):
    """用户创建模式"""
    username: str
    email: Optional[EmailStr] = None
    phone: str
    password: str
    role: Optional[UserRole] = UserRole.USER


class UserLogin(BaseModel):
    """用户登录模式"""
    username: str
    password: str


class UserResponse(BaseModel):
    """用户响应模式"""
    id: int
    username: str
    email: Optional[str] = None
    phone: str
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """令牌响应模式"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ForgotPasswordRequest(BaseModel):
    """忘记密码请求模式"""
    phone: str


class ResetPasswordRequest(BaseModel):
    """重置密码请求模式"""
    token: str
    new_password: str


class ForgotPasswordResponse(BaseModel):
    """忘记密码响应模式"""
    message: str
    reset_token: str
