from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from models.patent import Patent
from schemas.patent import PatentCreate, PatentUpdate


def get_patents(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    inventors: Optional[str] = None,
    patent_type: Optional[str] = None,
    application_number: Optional[str] = None,
    authorization_number: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> Tuple[List[Patent], int]:
    """
    获取专利列表（支持分页、筛选、排序）
    
    Args:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 返回的记录数
        title: 标题关键词（模糊匹配）
        inventors: 发明人关键词（模糊匹配）
        patent_type: 专利类型（精确匹配）
        application_number: 申请号（模糊匹配）
        authorization_number: 授权号（模糊匹配）
        sort_by: 排序字段
        sort_order: 排序方向（asc/desc）
    
    Returns:
        (专利列表, 总记录数)
    """
    query = db.query(Patent)
    
    # 应用筛选条件
    if title:
        query = query.filter(Patent.title.contains(title))
    if inventors:
        query = query.filter(Patent.inventors.contains(inventors))
    if patent_type:
        query = query.filter(Patent.patent_type == patent_type)
    if application_number:
        query = query.filter(Patent.application_number.contains(application_number))
    if authorization_number:
        query = query.filter(Patent.authorization_number.contains(authorization_number))
    
    # 获取总数
    total = query.count()
    
    # 应用排序
    sort_column = getattr(Patent, sort_by, Patent.created_at)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # 应用分页
    patents = query.offset(skip).limit(limit).all()
    
    return patents, total


def get_patent_by_id(db: Session, patent_id: int) -> Patent:
    """根据ID获取专利"""
    patent = db.query(Patent).filter(Patent.id == patent_id).first()
    if not patent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"专利ID {patent_id} 不存在"
        )
    return patent


def create_patent(db: Session, patent_create: PatentCreate) -> Patent:
    """创建专利"""
    # 检查申请号是否已存在（如果提供了申请号）
    if patent_create.application_number:
        existing_patent = db.query(Patent).filter(
            Patent.application_number == patent_create.application_number
        ).first()
        if existing_patent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"申请号 {patent_create.application_number} 已存在"
            )
    
    # 检查授权号是否已存在（如果提供了授权号）
    if patent_create.authorization_number:
        existing_patent = db.query(Patent).filter(
            Patent.authorization_number == patent_create.authorization_number
        ).first()
        if existing_patent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"授权号 {patent_create.authorization_number} 已存在"
            )
    
    # 创建新专利
    db_patent = Patent(**patent_create.model_dump())
    db.add(db_patent)
    db.commit()
    db.refresh(db_patent)
    return db_patent


def update_patent(db: Session, patent_id: int, patent_update: PatentUpdate) -> Patent:
    """更新专利"""
    db_patent = get_patent_by_id(db, patent_id)
    
    # 如果更新申请号，检查是否与其他专利冲突
    if patent_update.application_number and patent_update.application_number != db_patent.application_number:
        existing_patent = db.query(Patent).filter(
            Patent.application_number == patent_update.application_number,
            Patent.id != patent_id
        ).first()
        if existing_patent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"申请号 {patent_update.application_number} 已被其他专利使用"
            )
    
    # 如果更新授权号，检查是否与其他专利冲突
    if patent_update.authorization_number and patent_update.authorization_number != db_patent.authorization_number:
        existing_patent = db.query(Patent).filter(
            Patent.authorization_number == patent_update.authorization_number,
            Patent.id != patent_id
        ).first()
        if existing_patent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"授权号 {patent_update.authorization_number} 已被其他专利使用"
            )
    
    # 更新字段
    update_data = patent_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_patent, field, value)
    
    db.commit()
    db.refresh(db_patent)
    return db_patent


def delete_patent(db: Session, patent_id: int) -> None:
    """删除专利"""
    db_patent = get_patent_by_id(db, patent_id)
    db.delete(db_patent)
    db.commit()
    return None
