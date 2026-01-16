from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.sql import func
import enum
from config.database import Base


class PatentType(str, enum.Enum):
    """专利类型枚举"""
    INVENTION = "invention"  # 发明专利
    UTILITY_MODEL = "utility_model"  # 实用新型
    DESIGN = "design"  # 外观设计


class Patent(Base):
    """专利模型"""
    __tablename__ = "patents"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_number = Column(String(50), unique=True, index=True, nullable=True, comment="申请号")
    authorization_number = Column(String(50), unique=True, index=True, nullable=True, comment="授权号")
    title = Column(String(500), nullable=False, index=True, comment="专利名称")
    inventors = Column(Text, nullable=True, comment="发明人列表（JSON格式）")
    patent_type = Column(Enum(PatentType), nullable=True, comment="专利类型")
    application_date = Column(DateTime, nullable=True, index=True, comment="申请日期")
    authorization_date = Column(DateTime, nullable=True, index=True, comment="授权日期")
    abstract = Column(Text, nullable=True, comment="摘要")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Patent(id={self.id}, title={self.title[:50]}...)>"

