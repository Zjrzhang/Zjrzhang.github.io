from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PaperCreate(BaseModel):
    """论文创建模式"""
    title: str
    authors: Optional[str] = None
    journal_conference: Optional[str] = None
    publish_year: Optional[int] = None
    impact_factor: Optional[float] = None
    partition: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None


class PaperUpdate(BaseModel):
    """论文更新模式"""
    title: Optional[str] = None
    authors: Optional[str] = None
    journal_conference: Optional[str] = None
    publish_year: Optional[int] = None
    impact_factor: Optional[float] = None
    partition: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None


class PaperResponse(BaseModel):
    """论文响应模式"""
    id: int
    title: str
    authors: Optional[str]
    journal_conference: Optional[str]
    publish_year: Optional[int]
    impact_factor: Optional[float]
    partition: Optional[str]
    doi: Optional[str]
    abstract: Optional[str]
    keywords: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaperListResponse(BaseModel):
    """论文列表响应模式"""
    items: List[PaperResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

