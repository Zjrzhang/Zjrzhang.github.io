from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from config.database import get_db
from schemas.patent import (
    PatentCreate,
    PatentUpdate,
    PatentResponse,
    PatentListResponse
)
from services.patent_service import (
    get_patents,
    get_patent_by_id,
    create_patent,
    update_patent,
    delete_patent
)
from api.auth import get_current_user
from models.user import User

router = APIRouter()


@router.get("", response_model=PatentListResponse, summary="获取专利列表")
def list_patents(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    title: Optional[str] = Query(None, description="标题关键词"),
    inventors: Optional[str] = Query(None, description="发明人关键词"),
    patent_type: Optional[str] = Query(None, description="专利类型"),
    application_number: Optional[str] = Query(None, description="申请号"),
    authorization_number: Optional[str] = Query(None, description="授权号"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取专利列表
    
    - 支持分页查询
    - 支持按标题、发明人、专利类型、申请号、授权号筛选
    - 支持排序
    """
    skip = (page - 1) * page_size
    patents, total = get_patents(
        db=db,
        skip=skip,
        limit=page_size,
        title=title,
        inventors=inventors,
        patent_type=patent_type,
        application_number=application_number,
        authorization_number=authorization_number,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return PatentListResponse(
        items=[PatentResponse.model_validate(patent) for patent in patents],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{patent_id}", response_model=PatentResponse, summary="获取专利详情")
def get_patent(
    patent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据ID获取专利详情"""
    patent = get_patent_by_id(db, patent_id)
    return PatentResponse.model_validate(patent)


@router.post("", response_model=PatentResponse, status_code=status.HTTP_201_CREATED, summary="创建专利")
def create_new_patent(
    patent_create: PatentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新专利"""
    try:
        patent = create_patent(db, patent_create)
        return PatentResponse.model_validate(patent)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建专利失败: {str(e)}"
        )


@router.put("/{patent_id}", response_model=PatentResponse, summary="更新专利")
def update_existing_patent(
    patent_id: int,
    patent_update: PatentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新专利信息"""
    try:
        patent = update_patent(db, patent_id, patent_update)
        return PatentResponse.model_validate(patent)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新专利失败: {str(e)}"
        )


@router.delete("/{patent_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除专利")
def delete_existing_patent(
    patent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除专利"""
    try:
        delete_patent(db, patent_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除专利失败: {str(e)}"
        )
