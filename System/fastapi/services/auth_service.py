from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.security import verify_password, get_password_hash, create_access_token, decode_access_token
from config.settings import settings


def create_user(db: Session, user_create: UserCreate) -> User:
    """创建用户"""
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user_create.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查手机号是否已存在
    db_user = db.query(User).filter(User.phone == user_create.phone).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已存在"
        )
    
    # 检查邮箱是否已存在（如果提供了邮箱）
    if user_create.email:
        db_user = db.query(User).filter(User.email == user_create.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
    
    # 创建新用户
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        phone=user_create.phone,
        password_hash=hashed_password,
        role=user_create.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> User:
    """验证用户 - 支持通过用户名或手机号登录"""
    # 先尝试通过用户名查找
    user = db.query(User).filter(User.username == username).first()
    # 如果用户名不存在，尝试通过手机号查找
    if not user:
        user = db.query(User).filter(User.phone == username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名/手机号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名/手机号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    """根据ID获取用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user


def get_user_by_phone(db: Session, phone: str) -> User:
    """根据手机号获取用户"""
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该手机号未注册"
        )
    return user


def generate_reset_token(user_id: int) -> str:
    """生成密码重置令牌（有效期30分钟）"""
    expires_delta = timedelta(minutes=30)
    reset_token = create_access_token(
        data={"sub": str(user_id), "type": "password_reset"},  # sub必须是字符串
        expires_delta=expires_delta
    )
    return reset_token


def verify_reset_token(token: str) -> int:
    """验证重置令牌并返回用户ID"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效或过期的重置令牌"
        )
    
    token_type = payload.get("type")
    if token_type != "password_reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的重置令牌"
        )
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的重置令牌"
        )
    
    # 将字符串转换为整数
    try:
        user_id: int = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的重置令牌"
        )
    
    return user_id


def reset_user_password(db: Session, user_id: int, new_password: str) -> User:
    """重置用户密码"""
    user = get_user_by_id(db, user_id)
    user.password_hash = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user

