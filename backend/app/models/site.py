"""RSS 크롤링 사이트 모델"""

from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from enum import Enum


class SiteStatus(str, Enum):
    """사이트 상태"""
    ACTIVE = "active"      # 활성 (크롤링 중)
    INACTIVE = "inactive"  # 비활성 (크롤링 중지)
    ERROR = "error"        # 에러 (크롤링 실패 지속)


class Site(BaseModel):
    """RSS 크롤링 사이트"""
    id: Optional[str] = None
    name: str                          # 사이트 이름 (예: "Microsoft Blogs")
    url: str                           # 사이트 URL (예: "https://blogs.microsoft.com/")
    rss_url: str                       # RSS 피드 URL (예: "https://blogs.microsoft.com/feed/")
    crawl_interval: int = 30           # 크롤링 주기 (분 단위, 기본 30분)
    status: SiteStatus = SiteStatus.ACTIVE  # 사이트 상태
    
    # 통계
    last_crawled_at: Optional[datetime] = None   # 마지막 크롤링 시간
    next_crawl_at: Optional[datetime] = None     # 다음 크롤링 예정 시간
    total_crawls: int = 0                        # 총 크롤링 횟수
    success_count: int = 0                       # 성공 횟수
    error_count: int = 0                         # 실패 횟수
    total_posts_found: int = 0                   # 발견된 총 게시물 수
    
    # 메타데이터
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Microsoft Blogs",
                "url": "https://blogs.microsoft.com/",
                "rss_url": "https://blogs.microsoft.com/feed/",
                "crawl_interval": 30,
                "status": "active"
            }
        }


class SiteCreate(BaseModel):
    """사이트 생성 요청"""
    name: str
    url: str
    rss_url: str
    crawl_interval: int = 30
    status: SiteStatus = SiteStatus.INACTIVE  # 기본값: 비활성 (수동으로 활성화)


class SiteUpdate(BaseModel):
    """사이트 수정 요청"""
    name: Optional[str] = None
    url: Optional[str] = None
    rss_url: Optional[str] = None
    crawl_interval: Optional[int] = None
    status: Optional[SiteStatus] = None


class SiteResponse(BaseModel):
    """사이트 응답"""
    id: str
    name: str
    url: str
    rss_url: str
    crawl_interval: int
    status: SiteStatus
    last_crawled_at: Optional[datetime]
    next_crawl_at: Optional[datetime]
    total_crawls: int
    success_count: int
    error_count: int
    total_posts_found: int
    created_at: datetime
    updated_at: datetime

