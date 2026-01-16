from sqlalchemy import create_engine
from config.database import Base, engine
from config.settings import settings


def init_db():
    """初始化数据库，创建所有表"""
    # 导入所有模型，确保它们被注册到Base.metadata
    from models import user, paper, patent, project, personnel
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功！")


def drop_db():
    """删除所有表（谨慎使用）"""
    Base.metadata.drop_all(bind=engine)
    print("数据库表删除成功！")

