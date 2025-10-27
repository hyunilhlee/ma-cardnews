"""크롤링 로그 모델"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CrawlStatus(str, Enum):
    """크롤링 상태"""
    SUCCESS = "success"    # 성공
    PARTIAL = "partial"    # 부분 성공 (일부 게시물 처리 실패)
    FAILED = "failed"      # 실패
    RUNNING = "running"    # 실행 중


class CrawlLog(BaseModel):
    """크롤링 로그"""
    id: Optional[str] = None
    site_id: str                       # 크롤링한 사이트 ID
    site_name: str                     # 사이트 이름 (캐시)
    
    # 크롤링 결과
    status: CrawlStatus                # 크롤링 상태
    posts_found: int = 0               # 발견된 게시물 수
    new_posts: int = 0                 # 새로운 게시물 수
    projects_created: int = 0          # 생성된 프로젝트 수
    
    # 에러 정보
    error_message: Optional[str] = None
    error_details: Optional[dict] = None
    
    # 처리 시간
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    
    # 발견된 게시물 목록 (제목 & URL)
    post_titles: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "site_id": "site123",
                "site_name": "Microsoft Blogs",
                "status": "success",
                "posts_found": 5,
                "new_posts": 2,
                "projects_created": 2,
                "started_at": "2025-10-27T10:00:00Z",
                "completed_at": "2025-10-27T10:00:15Z",
                "duration_seconds": 15.3
            }
        }


class CrawlLogCreate(BaseModel):
    """크롤링 로그 생성"""
    site_id: str
    site_name: str
    status: CrawlStatus = CrawlStatus.RUNNING
    started_at: datetime = datetime.now()


class CrawlLogUpdate(BaseModel):
    """크롤링 로그 업데이트"""
    status: Optional[CrawlStatus] = None
    posts_found: Optional[int] = None
    new_posts: Optional[int] = None
    projects_created: Optional[int] = None
    error_message: Optional[str] = None
    error_details: Optional[dict] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    post_titles: Optional[List[str]] = None


class CrawlLogResponse(BaseModel):
    """크롤링 로그 응답"""
    id: str
    site_id: str
    site_name: str
    status: CrawlStatus
    posts_found: int
    new_posts: int
    projects_created: int
    error_message: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    post_titles: List[str]

