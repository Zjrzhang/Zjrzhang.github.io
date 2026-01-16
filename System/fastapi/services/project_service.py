from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from models.project import Project
from schemas.project import ProjectCreate, ProjectUpdate


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    project_number: Optional[str] = None,
    title: Optional[str] = None,
    project_type: Optional[str] = None,
    principal_investigator: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> Tuple[List[Project], int]:
    """
    获取项目列表（支持分页、筛选、排序）
    
    Args:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 返回的记录数
        project_number: 项目编号（模糊匹配）
        title: 项目名称关键词（模糊匹配）
        project_type: 项目类型（精确匹配）
        principal_investigator: 负责人（模糊匹配）
        status: 项目状态（精确匹配）
        sort_by: 排序字段
        sort_order: 排序方向（asc/desc）
    
    Returns:
        (项目列表, 总记录数)
    """
    query = db.query(Project)
    
    # 应用筛选条件
    if project_number:
        query = query.filter(Project.project_number.contains(project_number))
    if title:
        query = query.filter(Project.title.contains(title))
    if project_type:
        query = query.filter(Project.project_type == project_type)
    if principal_investigator:
        query = query.filter(Project.principal_investigator.contains(principal_investigator))
    if status:
        query = query.filter(Project.status == status)
    
    # 获取总数
    total = query.count()
    
    # 应用排序
    sort_column = getattr(Project, sort_by, Project.created_at)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # 应用分页
    projects = query.offset(skip).limit(limit).all()
    
    return projects, total


def get_project_by_id(db: Session, project_id: int) -> Project:
    """根据ID获取项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"项目ID {project_id} 不存在"
        )
    return project


def create_project(db: Session, project_create: ProjectCreate) -> Project:
    """创建项目"""
    # 检查项目编号是否已存在
    existing_project = db.query(Project).filter(
        Project.project_number == project_create.project_number
    ).first()
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"项目编号 {project_create.project_number} 已存在"
        )
    
    # 创建新项目
    db_project = Project(**project_create.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project_update: ProjectUpdate) -> Project:
    """更新项目"""
    db_project = get_project_by_id(db, project_id)
    
    # 如果更新项目编号，检查是否与其他项目冲突
    if project_update.project_number and project_update.project_number != db_project.project_number:
        existing_project = db.query(Project).filter(
            Project.project_number == project_update.project_number,
            Project.id != project_id
        ).first()
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"项目编号 {project_update.project_number} 已被其他项目使用"
            )
    
    # 更新字段
    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> None:
    """删除项目"""
    db_project = get_project_by_id(db, project_id)
    db.delete(db_project)
    db.commit()
    return None
