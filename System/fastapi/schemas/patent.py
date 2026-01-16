from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.patent import PatentType


class PatentCreate(BaseModel):
    """专利创建模式"""
    application_number: Optional[str] = None
    authorization_number: Optional[str] = None
    title: str
    inventors: Optional[str] = None
    patent_type: Optional[PatentType] = None
    application_date: Optional[datetime] = None
    authorization_date: Optional[datetime] = None
    abstract: Optional[str] = None


class PatentUpdate(BaseModel):
    """专利更新模式"""
    application_number: Optional[str] = None
    authorization_number: Optional[str] = None
    title: Optional[str] = None
    inventors: Optional[str] = None
    patent_type: Optional[PatentType] = None
    application_date: Optional[datetime] = None
    authorization_date: Optional[datetime] = None
    abstract: Optional[str] = None


class PatentResponse(BaseModel):
    """专利响应模式"""
    id: int
    application_number: Optional[str]
    authorization_number: Optional[str]
    title: str
    inventors: Optional[str]
    patent_type: Optional[PatentType]
    application_date: Optional[datetime]
    authorization_date: Optional[datetime]
    abstract: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PatentListResponse(BaseModel):
    """专利列表响应模式"""
    items: List[PatentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

