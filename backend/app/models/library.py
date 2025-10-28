"""RSS Library 관련 Pydantic 모델"""

from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime


class FeedSource(BaseModel):
    """피드 소스 정보"""
    site_id: Optional[str] = None
    site_name: str
    site_url: str


class LibraryFeedItem(BaseModel):
    """RSS Library 피드 아이템"""
    id: str
    type: Literal['project', 'rss_post']  # 프로젝트 또는 RSS 게시물
    title: str
    title_original: Optional[str] = None  # 원본 제목 (영문 등)
    source: FeedSource
    keywords: List[str] = []
    summary: str
    published_at: Optional[datetime] = None
    url: str
    has_cardnews: bool  # 카드뉴스 생성 여부
    project_id: Optional[str] = None  # 카드뉴스 프로젝트 ID (있는 경우)
    status: Optional[Literal['draft', 'summarized', 'completed']] = None
    is_new: bool = False  # 24시간 이내 여부
    
    class Config:
        from_attributes = True


class LibraryFeedResponse(BaseModel):
    """RSS Library 피드 응답"""
    total: int
    page: int
    page_size: int
    items: List[LibraryFeedItem]


class CreateCardnewsRequest(BaseModel):
    """RSS 게시물에서 카드뉴스 생성 요청"""
    rss_post_id: str
    site_id: str
    url: str
    title: str
    content: str


class CreateCardnewsResponse(BaseModel):
    """카드뉴스 생성 응답"""
    project_id: str
    status: Literal['draft', 'summarized', 'completed']

