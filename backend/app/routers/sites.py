"""Sites API - RSS 사이트 관리"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
import logging

from app.models.site import Site, SiteCreate, SiteUpdate, SiteResponse
from app.utils.firebase import (
    create_site,
    get_site,
    get_all_sites,
    update_site,
    delete_site,
    get_crawl_logs
)
from app.services.rss_service import RSSService
from app.services.scheduler_service import get_scheduler
from app.services.crawler import crawl_site_job

router = APIRouter(prefix="/api/sites", tags=["sites"])
logger = logging.getLogger(__name__)
rss_service = RSSService()


@router.post("", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
async def create_new_site(site: SiteCreate):
    """
    새로운 RSS 사이트 등록
    
    - **name**: 사이트 이름
    - **url**: 사이트 URL
    - **rss_url**: RSS 피드 URL
    - **crawl_interval**: 크롤링 주기 (분)
    - **status**: active/inactive
    """
    try:
        logger.info(f"Creating new site: {site.name}")
        
        # RSS URL 검증
        validation = rss_service.validate_rss_url(site.rss_url)
        if not validation['valid']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid RSS URL: {validation.get('error', 'Unknown error')}"
            )
        
        # 사이트 생성
        site_data = site.model_dump()
        created_site = create_site(site_data)
        
        # 활성 상태면 스케줄러에 작업 등록
        if site.status == 'active':
            try:
                scheduler = get_scheduler()
                scheduler.add_site_job(
                    site_id=created_site['id'],
                    site_name=created_site['name'],
                    rss_url=created_site['rss_url'],
                    crawl_interval=created_site['crawl_interval'],
                    crawl_func=crawl_site_job
                )
                logger.info(f"Scheduler job added for site: {created_site['id']}")
            except Exception as e:
                logger.warning(f"Failed to add scheduler job: {str(e)}")
        
        logger.info(f"Site created successfully: {created_site['id']}")
        return SiteResponse(**created_site)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create site: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create site: {str(e)}"
        )


@router.get("", response_model=List[SiteResponse])
async def list_sites():
    """
    모든 RSS 사이트 목록 조회
    
    최근 생성순으로 정렬됨
    """
    try:
        logger.info("Fetching all sites")
        sites = get_all_sites()
        
        return [SiteResponse(**site) for site in sites]
        
    except Exception as e:
        logger.error(f"Failed to fetch sites: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch sites: {str(e)}"
        )


@router.get("/{site_id}", response_model=SiteResponse)
async def get_site_by_id(site_id: str):
    """
    특정 RSS 사이트 조회
    
    - **site_id**: 사이트 ID
    """
    try:
        logger.info(f"Fetching site: {site_id}")
        site = get_site(site_id)
        
        if not site:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Site not found: {site_id}"
            )
        
        return SiteResponse(**site)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch site {site_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch site: {str(e)}"
        )


@router.put("/{site_id}", response_model=SiteResponse)
async def update_site_by_id(site_id: str, site: SiteUpdate):
    """
    RSS 사이트 정보 수정
    
    - **site_id**: 사이트 ID
    - 수정할 필드만 전송 (부분 수정 가능)
    """
    try:
        logger.info(f"Updating site: {site_id}")
        
        # 사이트 존재 확인
        existing_site = get_site(site_id)
        if not existing_site:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Site not found: {site_id}"
            )
        
        # RSS URL 변경 시 검증
        if site.rss_url and site.rss_url != existing_site.get('rss_url'):
            validation = rss_service.validate_rss_url(site.rss_url)
            if not validation['valid']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid RSS URL: {validation.get('error', 'Unknown error')}"
                )
        
        # 사이트 수정
        update_data = site.model_dump(exclude_unset=True)
        updated_site = update_site(site_id, update_data)
        
        # 스케줄러 작업 업데이트
        try:
            scheduler = get_scheduler()
            
            # 상태 변경 시
            if site.status:
                if site.status == 'active':
                    # 활성화: 작업 추가 또는 재개
                    scheduler.add_site_job(
                        site_id=updated_site['id'],
                        site_name=updated_site['name'],
                        rss_url=updated_site['rss_url'],
                        crawl_interval=updated_site['crawl_interval'],
                        crawl_func=crawl_site_job
                    )
                    logger.info(f"Scheduler job activated for site: {site_id}")
                else:
                    # 비활성화 또는 에러: 작업 제거
                    scheduler.remove_site_job(site_id)
                    logger.info(f"Scheduler job removed for site: {site_id}")
            
            # 크롤링 주기 변경 시 (활성 상태인 경우만)
            elif site.crawl_interval and updated_site.get('status') == 'active':
                scheduler.update_site_job(
                    site_id=updated_site['id'],
                    site_name=updated_site['name'],
                    rss_url=updated_site['rss_url'],
                    crawl_interval=updated_site['crawl_interval'],
                    crawl_func=crawl_site_job
                )
                logger.info(f"Scheduler job updated for site: {site_id}")
                
        except Exception as e:
            logger.warning(f"Failed to update scheduler job: {str(e)}")
        
        logger.info(f"Site updated successfully: {site_id}")
        return SiteResponse(**updated_site)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update site {site_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update site: {str(e)}"
        )


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site_by_id(site_id: str):
    """
    RSS 사이트 삭제
    
    - **site_id**: 사이트 ID
    """
    try:
        logger.info(f"Deleting site: {site_id}")
        
        # 사이트 존재 확인
        existing_site = get_site(site_id)
        if not existing_site:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Site not found: {site_id}"
            )
        
        # 스케줄러 작업 제거
        try:
            scheduler = get_scheduler()
            scheduler.remove_site_job(site_id)
            logger.info(f"Scheduler job removed for site: {site_id}")
        except Exception as e:
            logger.warning(f"Failed to remove scheduler job: {str(e)}")
        
        # 사이트 삭제
        delete_site(site_id)
        
        logger.info(f"Site deleted successfully: {site_id}")
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete site {site_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete site: {str(e)}"
        )


@router.post("/validate-rss", status_code=status.HTTP_200_OK)
async def validate_rss(rss_url: str):
    """
    RSS URL 검증
    
    - **rss_url**: 검증할 RSS 피드 URL
    
    Returns:
        {
            "valid": bool,
            "title": str,
            "description": str,
            "total_entries": int,
            "error": str (if not valid)
        }
    """
    try:
        logger.info(f"Validating RSS URL: {rss_url}")
        result = rss_service.validate_rss_url(rss_url)
        
        return result
        
    except Exception as e:
        logger.error(f"RSS validation failed: {str(e)}")
        return {
            "valid": False,
            "error": str(e)
        }


@router.post("/{site_id}/trigger-crawl", status_code=status.HTTP_202_ACCEPTED)
async def trigger_manual_crawl(site_id: str):
    """
    수동 크롤링 트리거
    
    - **site_id**: 사이트 ID
    
    스케줄러를 통해 즉시 크롤링 실행
    """
    try:
        logger.info(f"Manual crawl triggered for site: {site_id}")
        
        # 사이트 존재 확인
        site = get_site(site_id)
        if not site:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Site not found: {site_id}"
            )
        
        # 스케줄러를 통해 즉시 실행
        try:
            scheduler = get_scheduler()
            
            # 작업이 등록되어 있으면 즉시 실행
            job_info = scheduler.get_job_info(site_id)
            if job_info:
                scheduler.trigger_site_job_now(site_id)
                logger.info(f"Existing job triggered for site: {site_id}")
            else:
                # 작업이 없으면 직접 실행 (비활성 사이트)
                logger.info(f"No job found, running crawler directly for site: {site_id}")
                result = crawl_site_job(site_id)
                
                if result['status'] == 'failed':
                    logger.warning(f"Manual crawl failed: {result.get('error', 'Unknown')}")
                    
        except Exception as e:
            logger.error(f"Failed to trigger crawl: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to trigger crawl: {str(e)}"
            )
        
        return {
            "message": f"Crawl job triggered for site: {site['name']}",
            "site_id": site_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger crawl for site {site_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger crawl: {str(e)}"
        )


@router.get("/{site_id}/crawl-logs")
async def get_site_crawl_logs(site_id: str, limit: int = 20):
    """
    특정 사이트의 크롤링 로그 조회
    
    - **site_id**: 사이트 ID
    - **limit**: 조회할 로그 수 (기본: 20)
    
    최근 크롤링 이력과 발견된 게시물 정보 반환
    """
    try:
        logger.info(f"Fetching crawl logs for site: {site_id}")
        
        # 사이트 존재 확인
        site = get_site(site_id)
        if not site:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Site not found: {site_id}"
            )
        
        # 크롤링 로그 조회
        logs = get_crawl_logs(site_id=site_id, limit=limit)
        
        logger.info(f"Found {len(logs)} crawl logs for site: {site_id}")
        
        return {
            "site_id": site_id,
            "site_name": site['name'],
            "total_logs": len(logs),
            "logs": logs
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch crawl logs for site {site_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch crawl logs: {str(e)}"
        )


@router.get("/crawl-logs/all")
async def get_all_crawl_logs(limit: int = 50):
    """
    모든 사이트의 크롤링 로그 조회
    
    - **limit**: 조회할 로그 수 (기본: 50)
    
    전체 크롤링 이력 반환
    """
    try:
        logger.info(f"Fetching all crawl logs (limit: {limit})")
        
        # 모든 크롤링 로그 조회
        logs = get_crawl_logs(site_id=None, limit=limit)
        
        logger.info(f"Found {len(logs)} total crawl logs")
        
        return {
            "total_logs": len(logs),
            "logs": logs
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch all crawl logs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch crawl logs: {str(e)}"
        )

