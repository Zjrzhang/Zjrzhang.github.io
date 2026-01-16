from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from config.database import get_db
from schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse
)
from services.project_service import (
    get_projects,
    get_project_by_id,
    create_project,
    update_project,
    delete_project
)
from api.auth import get_current_user
from models.user import User

router = APIRouter()


@router.get("", response_model=ProjectListResponse, summary="获取项目列表")
def list_projects(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    project_number: Optional[str] = Query(None, description="项目编号关键词"),
    title: Optional[str] = Query(None, description="项目名称关键词"),
    project_type: Optional[str] = Query(None, description="项目类型"),
    principal_investigator: Optional[str] = Query(None, description="负责人关键词"),
    status: Optional[str] = Query(None, description="项目状态"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取项目列表
    
    - 支持分页查询
    - 支持按项目编号、名称、类型、负责人、状态筛选
    - 支持排序
    """
    skip = (page - 1) * page_size
    projects, total = get_projects(
        db=db,
        skip=skip,
        limit=page_size,
        project_number=project_number,
        title=title,
        project_type=project_type,
        principal_investigator=principal_investigator,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return ProjectListResponse(
        items=[ProjectResponse.model_validate(project) for project in projects],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{project_id}", response_model=ProjectResponse, summary="获取项目详情")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据ID获取项目详情"""
    project = get_project_by_id(db, project_id)
    return ProjectResponse.model_validate(project)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, summary="创建项目")
def create_new_project(
    project_create: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新项目"""
    try:
        project = create_project(db, project_create)
        return ProjectResponse.model_validate(project)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建项目失败: {str(e)}"
        )


@router.put("/{project_id}", response_model=ProjectResponse, summary="更新项目")
def update_existing_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新项目信息"""
    try:
        project = update_project(db, project_id, project_update)
        return ProjectResponse.model_validate(project)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新项目失败: {str(e)}"
        )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除项目")
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除项目"""
    try:
        delete_project(db, project_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除项目失败: {str(e)}"
        )
