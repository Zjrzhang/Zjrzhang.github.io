from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PersonnelCreate(BaseModel):
    """人员创建模式"""
    name: str
    unit: Optional[str] = None
    title: Optional[str] = None
    research_direction: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class PersonnelUpdate(BaseModel):
    """人员更新模式"""
    name: Optional[str] = None
    unit: Optional[str] = None
    title: Optional[str] = None
    research_direction: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class PersonnelResponse(BaseModel):
    """人员响应模式"""
    id: int
    name: str
    unit: Optional[str]
    title: Optional[str]
    research_direction: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

