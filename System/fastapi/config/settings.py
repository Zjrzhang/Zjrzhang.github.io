from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/research_management?charset=utf8mb4"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 应用配置
    DEBUG: bool = True
    PROJECT_NAME: str = "科研成果管理系统"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

