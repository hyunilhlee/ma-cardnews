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

# CORS 설정 - 로컬 개발 및 프로덕션 도메인 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # 모든 Vercel 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase & 스케줄러 초기화
@app.on_event("startup")
async def startup_event():
    """앱 시작 시 Firebase 및 스케줄러 초기화"""
    # Firebase 초기화
    firebase.initialize_firebase()
    
    # Phase 2: 스케줄러 초기화 및 활성 사이트 로드
    try:
        from app.services.scheduler_service import init_scheduler
        from app.services.crawler import crawl_site_job
        from app.utils.firebase import get_all_sites
        
        # 스케줄러 시작
        scheduler = init_scheduler()
        
        # 활성 사이트 로드 및 작업 등록
        sites = get_all_sites()
        active_sites = [s for s in sites if s.get('status') == 'active']
        
        for site in active_sites:
            scheduler.add_site_job(
                site_id=site['id'],
                site_name=site['name'],
                rss_url=site['rss_url'],
                crawl_interval=site['crawl_interval'],
                crawl_func=crawl_site_job
            )
        
        logger = logging.getLogger(__name__)
        logger.info(f"Scheduler loaded {len(active_sites)} active sites")
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Scheduler initialization failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """앱 종료 시 스케줄러 종료"""
    try:
        from app.services.scheduler_service import shutdown_scheduler
        shutdown_scheduler()
        logger = logging.getLogger(__name__)
        logger.info("Scheduler shutdown completed")
    except:
        pass

# 라우터 등록
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(status.router, prefix="/api/status", tags=["status"])

# Phase 2: Sites 라우터
try:
    from app.routers import sites
    app.include_router(sites.router, tags=["sites"])
    logger = logging.getLogger(__name__)
    logger.info("Sites router registered")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"Sites router not available: {e}")

# Phase 2.5: Library 라우터
try:
    from app.routers import library
    app.include_router(library.router, tags=["library"])
    logger = logging.getLogger(__name__)
    logger.info("Library router registered")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"Library router not available: {e}")


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

