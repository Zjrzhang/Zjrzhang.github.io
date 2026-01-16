from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Enum
from sqlalchemy.sql import func
import enum
from config.database import Base


class ProjectType(str, enum.Enum):
    """项目类型枚举"""
    NATIONAL = "national"  # 国家级
    PROVINCIAL = "provincial"  # 省级
    MUNICIPAL = "municipal"  # 市级
    ENTERPRISE = "enterprise"  # 企业
    OTHER = "other"  # 其他


class Project(Base):
    """项目模型"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_number = Column(String(100), unique=True, index=True, nullable=False, comment="项目编号")
    project_type = Column(Enum(ProjectType), nullable=True, comment="项目类型")
    title = Column(String(500), nullable=False, index=True, comment="项目名称")
    principal_investigator = Column(String(100), nullable=True, index=True, comment="负责人")
    start_date = Column(DateTime, nullable=True, index=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, index=True, comment="结束日期")
    funding_amount = Column(Float, nullable=True, comment="资助金额")
    task_description = Column(Text, nullable=True, comment="任务书内容")
    status = Column(String(50), nullable=True, default="进行中", comment="项目状态")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Project(id={self.id}, project_number={self.project_number})>"

