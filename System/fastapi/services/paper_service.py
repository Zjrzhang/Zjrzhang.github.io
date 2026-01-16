from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from models.paper import Paper
from schemas.paper import PaperCreate, PaperUpdate


def get_papers(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    authors: Optional[str] = None,
    journal_conference: Optional[str] = None,
    publish_year: Optional[int] = None,
    partition: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> Tuple[List[Paper], int]:
    """
    获取论文列表（支持分页、筛选、排序）
    
    Args:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 返回的记录数
        title: 标题关键词（模糊匹配）
        authors: 作者关键词（模糊匹配）
        journal_conference: 期刊/会议名称（模糊匹配）
        publish_year: 发表年份（精确匹配）
        partition: 分区（精确匹配）
        sort_by: 排序字段
        sort_order: 排序方向（asc/desc）
    
    Returns:
        (论文列表, 总记录数)
    """
    query = db.query(Paper)
    
    # 应用筛选条件
    if title:
        query = query.filter(Paper.title.contains(title))
    if authors:
        query = query.filter(Paper.authors.contains(authors))
    if journal_conference:
        query = query.filter(Paper.journal_conference.contains(journal_conference))
    if publish_year:
        query = query.filter(Paper.publish_year == publish_year)
    if partition:
        query = query.filter(Paper.partition == partition)
    
    # 获取总数
    total = query.count()
    
    # 应用排序
    sort_column = getattr(Paper, sort_by, Paper.created_at)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # 应用分页
    papers = query.offset(skip).limit(limit).all()
    
    return papers, total


def get_paper_by_id(db: Session, paper_id: int) -> Paper:
    """根据ID获取论文"""
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"论文ID {paper_id} 不存在"
        )
    return paper


def create_paper(db: Session, paper_create: PaperCreate) -> Paper:
    """创建论文"""
    # 检查DOI是否已存在（如果提供了DOI）
    if paper_create.doi:
        existing_paper = db.query(Paper).filter(Paper.doi == paper_create.doi).first()
        if existing_paper:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"DOI {paper_create.doi} 已存在"
            )
    
    # 创建新论文
    db_paper = Paper(**paper_create.model_dump())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


def update_paper(db: Session, paper_id: int, paper_update: PaperUpdate) -> Paper:
    """更新论文"""
    db_paper = get_paper_by_id(db, paper_id)
    
    # 如果更新DOI，检查是否与其他论文冲突
    if paper_update.doi and paper_update.doi != db_paper.doi:
        existing_paper = db.query(Paper).filter(
            Paper.doi == paper_update.doi,
            Paper.id != paper_id
        ).first()
        if existing_paper:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"DOI {paper_update.doi} 已被其他论文使用"
            )
    
    # 更新字段
    update_data = paper_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_paper, field, value)
    
    db.commit()
    db.refresh(db_paper)
    return db_paper


def delete_paper(db: Session, paper_id: int) -> None:
    """删除论文"""
    db_paper = get_paper_by_id(db, paper_id)
    db.delete(db_paper)
    db.commit()
    return None
