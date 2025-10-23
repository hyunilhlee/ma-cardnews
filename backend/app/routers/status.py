"""
시스템 상태 확인 API 라우터
"""

from fastapi import APIRouter
from app.services.openai_status import check_api_status, get_usage_info
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/openai")
async def get_openai_status():
    """
    OpenAI API 연결 상태 확인
    """
    status = check_api_status()
    usage = get_usage_info()
    
    return {
        "api_status": status,
        "usage_info": usage
    }


@router.get("/system")
async def get_system_status():
    """
    전체 시스템 상태 확인
    """
    openai_status = check_api_status()
    
    return {
        "status": "healthy",
        "services": {
            "openai": openai_status,
            "backend": {
                "connected": True,
                "status": "정상",
                "message": "Backend API 정상 작동 중"
            }
        }
    }

