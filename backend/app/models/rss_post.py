"""RSS 게시물 모델 - DB 영구 저장용"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RSSPost(BaseModel):
    """RSS 게시물 (DB 저장용)"""
    id: str  # URL의 MD5 해시
    site_id: str  # 어느 사이트에서 크롤링했는지
    site_name: str
    title: str  # 한글 번역된 제목
    title_original: Optional[str] = None  # 원본 제목 (영문 등)
    url: str  # 원본 URL (unique)
    content: str  # 전체 콘텐츠
    summary: str  # AI 생성 요약 (한글, 8-12문장)
    keywords: List[str] = []  # AI 추출 키워드
    author: Optional[str] = None
    published_at: datetime  # 원본 게시 날짜
    crawled_at: datetime  # 크롤링된 날짜
    
    # 카드뉴스 생성 여부
    has_cardnews: bool = False
    project_id: Optional[str] = None  # 연결된 프로젝트 ID
    
    class Config:
        from_attributes = True


class RSSPostCreate(BaseModel):
    """RSS 게시물 생성 요청"""
    site_id: str
    site_name: str
    title: str
    title_original: Optional[str] = None
    url: str
    content: str
    summary: str
    keywords: List[str] = []
    author: Optional[str] = None
    published_at: datetime


class RSSPostResponse(BaseModel):
    """RSS 게시물 응답"""
    id: str
    site_id: str
    site_name: str
    title: str
    title_original: Optional[str] = None
    url: str
    content: str
    summary: str
    keywords: List[str] = []
    author: Optional[str] = None
    published_at: datetime
    crawled_at: datetime
    has_cardnews: bool
    project_id: Optional[str] = None
    
    class Config:
        from_attributes = True

