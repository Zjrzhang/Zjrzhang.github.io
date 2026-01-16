from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from config.database import Base


class FundingOrder(str, enum.Enum):
    """资助顺序枚举"""
    PRIMARY = "primary"  # 主要资助
    SECONDARY = "secondary"  # 次要资助
    OTHER = "other"  # 其他


class PaperProjectRelation(Base):
    """论文-项目关联表"""
    __tablename__ = "paper_project_relations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False, index=True, comment="论文ID")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID")
    funding_order = Column(Enum(FundingOrder), nullable=True, comment="资助顺序")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    # 唯一约束：同一论文和项目的组合只能有一条记录
    __table_args__ = (
        {"comment": "论文-项目关联表"},
    )


class PatentProjectRelation(Base):
    """专利-项目关联表"""
    __tablename__ = "patent_project_relations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patent_id = Column(Integer, ForeignKey("patents.id", ondelete="CASCADE"), nullable=False, index=True, comment="专利ID")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID")
    funding_order = Column(Enum(FundingOrder), nullable=True, comment="资助顺序")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    __table_args__ = (
        {"comment": "专利-项目关联表"},
    )


class AuthorPaperRelation(Base):
    """作者-论文关联表"""
    __tablename__ = "author_paper_relations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False, index=True, comment="人员ID")
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False, index=True, comment="论文ID")
    author_order = Column(Integer, nullable=True, comment="作者顺序（1为第一作者）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    __table_args__ = (
        {"comment": "作者-论文关联表"},
    )


class AuthorPatentRelation(Base):
    """发明人-专利关联表"""
    __tablename__ = "author_patent_relations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False, index=True, comment="人员ID")
    patent_id = Column(Integer, ForeignKey("patents.id", ondelete="CASCADE"), nullable=False, index=True, comment="专利ID")
    inventor_order = Column(Integer, nullable=True, comment="发明人顺序")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    __table_args__ = (
        {"comment": "发明人-专利关联表"},
    )


class PersonnelProjectRelation(Base):
    """人员-项目关联表"""
    __tablename__ = "personnel_project_relations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False, index=True, comment="人员ID")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID")
    role = Column(String(50), nullable=True, comment="角色（负责人、参与人等）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    __table_args__ = (
        {"comment": "人员-项目关联表"},
    )

