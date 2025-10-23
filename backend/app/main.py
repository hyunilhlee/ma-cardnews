"""FastAPI 애플리케이션 진입점"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import projects, chat, status
from app.utils import firebase
import logging

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# FastAPI 앱 초기화
app = FastAPI(
    title="CardNews AI API",
    description="AI 기반 카드뉴스 생성 API",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase 초기화
@app.on_event("startup")
async def startup_event():
    """앱 시작 시 Firebase 초기화"""
    firebase.initialize_firebase()

# 라우터 등록
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(status.router, prefix="/api/status", tags=["status"])


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "CardNews AI API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "openai_configured": bool(settings.OPENAI_API_KEY)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG
    )

