from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from config.database import Base


class Paper(Base):
    """论文模型"""
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(500), nullable=False, index=True, comment="论文标题")
    authors = Column(Text, nullable=True, comment="作者列表（JSON格式）")
    journal_conference = Column(String(200), nullable=True, index=True, comment="期刊/会议名称")
    publish_year = Column(Integer, nullable=True, index=True, comment="发表年份")
    impact_factor = Column(Float, nullable=True, comment="影响因子")
    partition = Column(String(10), nullable=True, comment="分区（如：Q1, Q2, Q3, Q4）")
    doi = Column(String(200), nullable=True, unique=True, comment="DOI")
    abstract = Column(Text, nullable=True, comment="摘要")
    keywords = Column(String(500), nullable=True, comment="关键词")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Paper(id={self.id}, title={self.title[:50]}...)>"

