from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from config.database import Base


class Personnel(Base):
    """人员模型"""
    __tablename__ = "personnel"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True, comment="姓名")
    unit = Column(String(200), nullable=True, index=True, comment="单位")
    title = Column(String(100), nullable=True, comment="职称")
    research_direction = Column(Text, nullable=True, comment="研究方向")
    email = Column(String(100), nullable=True, unique=True, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="电话")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Personnel(id={self.id}, name={self.name})>"

