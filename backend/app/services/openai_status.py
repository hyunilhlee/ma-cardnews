"""
OpenAI API 상태 확인 서비스
"""

import openai
from app.config import settings
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def check_api_status() -> Dict:
    """
    OpenAI API 연결 상태 확인
    
    Returns:
        상태 정보 딕셔너리
    """
    try:
        # 간단한 API 호출로 연결 테스트
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        
        return {
            "connected": True,
            "model": settings.OPENAI_MODEL,
            "status": "정상",
            "message": "OpenAI API 연결 정상"
        }
        
    except openai.AuthenticationError:
        logger.error("OpenAI API 인증 실패")
        return {
            "connected": False,
            "model": settings.OPENAI_MODEL,
            "status": "인증 실패",
            "message": "API 키가 유효하지 않습니다"
        }
    except openai.RateLimitError:
        logger.error("OpenAI API 사용량 초과")
        return {
            "connected": False,
            "model": settings.OPENAI_MODEL,
            "status": "사용량 초과",
            "message": "API 사용량이 초과되었습니다"
        }
    except Exception as e:
        logger.error(f"OpenAI API 연결 실패: {str(e)}")
        return {
            "connected": False,
            "model": settings.OPENAI_MODEL,
            "status": "연결 실패",
            "message": f"연결 오류: {str(e)}"
        }


def get_usage_info() -> Optional[Dict]:
    """
    OpenAI API 사용량 정보 조회
    
    Note: 현재 OpenAI API는 사용량을 직접 조회하는 엔드포인트를 제공하지 않습니다.
    실제 크레딧은 OpenAI 대시보드에서 확인해야 합니다.
    
    Returns:
        사용량 정보 (현재는 모의 데이터)
    """
    return {
        "note": "크레딧 정보는 OpenAI 대시보드에서 확인하세요",
        "dashboard_url": "https://platform.openai.com/usage"
    }

