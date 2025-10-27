"""프로젝트 관련 Pydantic 모델"""

from pydantic import BaseModel, field_validator
from typing import Optional, List, Literal
from datetime import datetime


class ProjectCreate(BaseModel):
    """프로젝트 생성 요청"""
    source_type: Literal['url', 'text', 'rss']  # Phase 2: 'rss' 추가
    source_content: str
    card_start_type: Literal['title', 'content'] = 'title'  # 기본값: 제목으로 시작
    model: str = 'gpt-4.1-nano'  # 사용할 AI 모델
    source_site_id: Optional[str] = None  # Phase 2: RSS 사이트 ID (자동 생성 시)
    
    @field_validator('source_content')
    @classmethod
    def validate_content_length(cls, v: str) -> str:
        """내용 길이 검증"""
        if len(v) > 10000:
            raise ValueError('텍스트는 10,000자를 초과할 수 없습니다.')
        if len(v.strip()) == 0:
            raise ValueError('내용이 비어있습니다.')
        return v


class ProjectResponse(BaseModel):
    """프로젝트 응답"""
    id: str
    source_type: str
    source_content: str
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    recommended_card_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    status: Literal['draft', 'summarized', 'completed']
    model: Optional[str] = 'gpt-4.1-nano'  # 사용된 AI 모델
    card_start_type: Optional[str] = 'title'  # 카드 시작 타입
    
    # Phase 2: 추가 필드
    source_site_id: Optional[str] = None  # RSS 사이트 ID
    source_site_name: Optional[str] = None  # RSS 사이트 이름 (캐시)
    version: int = 1  # 버전 (수정 시 증가)
    is_auto_generated: bool = False  # 자동 생성 여부
    last_error: Optional[str] = None  # 마지막 에러 메시지 (자동 생성 실패 시)
    
    class Config:
        from_attributes = True


class SummarizeRequest(BaseModel):
    """요약 요청"""
    max_length: int = 200


class SummarizeResponse(BaseModel):
    """요약 응답"""
    summary: str
    keywords: List[str]
    recommended_card_count: int

