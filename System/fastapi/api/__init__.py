from fastapi import APIRouter
from . import auth, papers, patents, projects

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(papers.router, prefix="/papers", tags=["论文管理"])
api_router.include_router(patents.router, prefix="/patents", tags=["专利管理"])
api_router.include_router(projects.router, prefix="/projects", tags=["项目管理"])

