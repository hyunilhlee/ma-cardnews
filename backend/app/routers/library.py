"""RSS Library API 라우터"""

from fastapi import APIRouter, Query, HTTPException, status
from datetime import datetime
from typing import Optional
import logging

from app.models.library import (
    LibraryFeedResponse,
    LibraryFeedItem,
    FeedSource,
    CreateCardnewsRequest,
    CreateCardnewsResponse
)
from app.services.library_service import get_library_service
from app.services.pipeline_service import AutoGenerationPipeline
from app.utils.firebase import get_site

router = APIRouter(prefix="/api/library", tags=["library"])
logger = logging.getLogger(__name__)


@router.get("/feed", response_model=LibraryFeedResponse)
async def get_library_feed(
    site_id: Optional[str] = Query(None, description="특정 사이트만 조회"),
    start_date: Optional[datetime] = Query(None, description="시작 날짜"),
    end_date: Optional[datetime] = Query(None, description="종료 날짜"),
    keyword: Optional[str] = Query(None, description="키워드 검색"),
    year_month: Optional[str] = Query(None, description="연월 필터 (YYYY-MM 형식)"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(20, ge=1, le=100, description="페이지 크기")
):
    """
    RSS Library 통합 피드 조회
    
    - 등록된 모든 RSS 사이트의 게시물을 시간순으로 조회
    - 카드뉴스가 생성된 게시물과 미생성 게시물 모두 포함
    - 필터링: 사이트별, 날짜별, 키워드별
    """
    try:
        logger.info(f"GET /api/library/feed - site_id={site_id}, keyword={keyword}, page={page}")
        
        library_service = get_library_service()
        
        result = await library_service.get_feed(
            site_id=site_id,
            start_date=start_date,
            end_date=end_date,
            keyword=keyword,
            year_month=year_month,
            page=page,
            page_size=page_size
        )
        
        # Pydantic 모델로 변환
        items = []
        for item in result['items']:
            items.append(LibraryFeedItem(
                id=item['id'],
                type=item['type'],
                title=item['title'],
                source=FeedSource(**item['source']),
                keywords=item['keywords'],
                summary=item['summary'],
                published_at=item['published_at'],
                url=item['url'],
                has_cardnews=item['has_cardnews'],
                project_id=item['project_id'],
                status=item['status'],
                is_new=item['is_new']
            ))
        
        return LibraryFeedResponse(
            total=result['total'],
            page=result['page'],
            page_size=result['page_size'],
            items=items
        )
        
    except Exception as e:
        logger.error(f"Failed to get library feed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get library feed: {str(e)}"
        )


@router.post("/create-cardnews", response_model=CreateCardnewsResponse)
async def create_cardnews_from_feed(request: CreateCardnewsRequest):
    """
    RSS Library에서 카드뉴스 생성
    
    - RSS 게시물을 카드뉴스 프로젝트로 변환
    - 자동 생성 파이프라인 실행 (스크래핑 → 요약 → 카드뉴스 생성)
    """
    try:
        logger.info(f"POST /api/library/create-cardnews - url={request.url}")
        
        # 사이트 정보 조회
        site = get_site(request.site_id)
        if not site:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Site not found: {request.site_id}"
            )
        
        # 자동 생성 파이프라인 실행
        pipeline = AutoGenerationPipeline(model='gpt-4.1-nano')
        
        # RSS 게시물 형식으로 변환
        post = {
            'id': request.rss_post_id,
            'title': request.title,
            'link': request.url,
            'content': request.content,
            'summary': '',
            'published': datetime.now(),
            'author': 'Unknown'
        }
        
        # 카드뉴스 생성
        project_id = await pipeline.generate_cardnews_from_post(
            post=post,
            site_id=request.site_id,
            site_name=site['name']
        )
        
        if not project_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate cardnews"
            )
        
        # 프로젝트 상태 조회
        from app.utils.firebase import get_project
        project = get_project(project_id)
        
        return CreateCardnewsResponse(
            project_id=project_id,
            status=project.get('status', 'draft')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create cardnews from feed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create cardnews: {str(e)}"
        )

