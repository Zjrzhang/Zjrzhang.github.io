from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.project import ProjectType


class ProjectCreate(BaseModel):
    """项目创建模式"""
    project_number: str
    project_type: Optional[ProjectType] = None
    title: str
    principal_investigator: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    funding_amount: Optional[float] = None
    task_description: Optional[str] = None
    status: Optional[str] = "进行中"


class ProjectUpdate(BaseModel):
    """项目更新模式"""
    project_number: Optional[str] = None
    project_type: Optional[ProjectType] = None
    title: Optional[str] = None
    principal_investigator: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    funding_amount: Optional[float] = None
    task_description: Optional[str] = None
    status: Optional[str] = None


class ProjectResponse(BaseModel):
    """项目响应模式"""
    id: int
    project_number: str
    project_type: Optional[ProjectType]
    title: str
    principal_investigator: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    funding_amount: Optional[float]
    task_description: Optional[str]
    status: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """项目列表响应模式"""
    items: List[ProjectResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

