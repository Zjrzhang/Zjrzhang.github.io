from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from config.database import get_db
from config.settings import settings
from schemas.user import UserCreate, UserResponse, Token, ForgotPasswordRequest, ResetPasswordRequest, ForgotPasswordResponse
from services.auth_service import (
    create_user, authenticate_user, get_user_by_id,
    get_user_by_phone, generate_reset_token, verify_reset_token, reset_user_password
)
from utils.security import create_access_token, decode_access_token
from models.user import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    # 在开发环境中打印token信息用于调试
    if settings.DEBUG:
        print(f"收到token: {token[:20] if token and len(token) > 20 else token}")
        print(f"Token长度: {len(token) if token else 0}")
    
    # 清理token
    if token:
        token = token.strip()
    
    payload = decode_access_token(token)
    if payload is None:
        if settings.DEBUG:
            print("Token解码失败: payload为None")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        if settings.DEBUG:
            print(f"Token payload中缺少sub字段: {payload}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 将字符串转换为整数
    try:
        user_id: int = int(user_id_str)
    except (ValueError, TypeError):
        if settings.DEBUG:
            print(f"Token payload中的sub字段无法转换为整数: {user_id_str}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_id(db, user_id)
    if not user:
        if settings.DEBUG:
            print(f"用户不存在: user_id={user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    user = create_user(db, user_create)
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录"""
    user = authenticate_user(db, form_data.username, form_data.password)
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},  # sub必须是字符串
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """忘记密码 - 发送重置令牌"""
    try:
        # 根据手机号查找用户
        user = get_user_by_phone(db, request.phone)
        
        # 生成重置令牌
        reset_token = generate_reset_token(user.id)
        
        # 在实际应用中，这里应该发送邮件或短信
        # 目前直接返回令牌（开发环境）
        return {
            "message": "重置令牌已生成，请使用该令牌重置密码",
            "reset_token": reset_token
        }
    except HTTPException as e:
        # 如果用户不存在，为了安全不泄露信息，返回通用错误
        # 但在开发环境中，我们可以返回更明确的错误
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="该手机号未注册"
            )
        raise


@router.post("/reset-password", response_model=UserResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """重置密码"""
    # 验证新密码长度
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码长度至少为6位"
        )
    
    # 验证重置令牌
    user_id = verify_reset_token(request.token)
    
    # 重置密码
    user = reset_user_password(db, user_id, request.new_password)
    
    return user

