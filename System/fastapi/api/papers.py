from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from config.database import get_db
from schemas.paper import (
    PaperCreate,
    PaperUpdate,
    PaperResponse,
    PaperListResponse
)
from services.paper_service import (
    get_papers,
    get_paper_by_id,
    create_paper,
    update_paper,
    delete_paper
)
from api.auth import get_current_user
from models.user import User

router = APIRouter()


@router.get("", response_model=PaperListResponse, summary="获取论文列表")
def list_papers(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    title: Optional[str] = Query(None, description="标题关键词"),
    authors: Optional[str] = Query(None, description="作者关键词"),
    journal_conference: Optional[str] = Query(None, description="期刊/会议名称"),
    publish_year: Optional[int] = Query(None, description="发表年份"),
    partition: Optional[str] = Query(None, description="分区（Q1/Q2/Q3/Q4）"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取论文列表
    
    - 支持分页查询
    - 支持按标题、作者、期刊、年份、分区筛选
    - 支持排序
    """
    skip = (page - 1) * page_size
    papers, total = get_papers(
        db=db,
        skip=skip,
        limit=page_size,
        title=title,
        authors=authors,
        journal_conference=journal_conference,
        publish_year=publish_year,
        partition=partition,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return PaperListResponse(
        items=[PaperResponse.model_validate(paper) for paper in papers],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{paper_id}", response_model=PaperResponse, summary="获取论文详情")
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据ID获取论文详情"""
    paper = get_paper_by_id(db, paper_id)
    return PaperResponse.model_validate(paper)


@router.post("", response_model=PaperResponse, status_code=status.HTTP_201_CREATED, summary="创建论文")
def create_new_paper(
    paper_create: PaperCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新论文"""
    try:
        paper = create_paper(db, paper_create)
        return PaperResponse.model_validate(paper)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建论文失败: {str(e)}"
        )


@router.put("/{paper_id}", response_model=PaperResponse, summary="更新论文")
def update_existing_paper(
    paper_id: int,
    paper_update: PaperUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新论文信息"""
    try:
        paper = update_paper(db, paper_id, paper_update)
        return PaperResponse.model_validate(paper)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新论文失败: {str(e)}"
        )


@router.delete("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除论文")
def delete_existing_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除论文"""
    try:
        delete_paper(db, paper_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除论文失败: {str(e)}"
        )
