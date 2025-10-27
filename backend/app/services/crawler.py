"""크롤러 - RSS 사이트 자동 크롤링 및 카드뉴스 생성"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import logging

from app.services.rss_service import RSSService
from app.utils.firebase import (
    get_site,
    update_site,
    create_crawl_log,
    update_crawl_log
)

logger = logging.getLogger(__name__)


class SiteCrawler:
    """RSS 사이트 크롤러"""
    
    def __init__(self):
        self.rss_service = RSSService()
    
    def crawl_site(self, site_id: str) -> Dict:
        """
        사이트 크롤링 실행
        
        Args:
            site_id: 사이트 ID
            
        Returns:
            크롤링 결과
            {
                'status': 'success' | 'failed',
                'posts_found': int,
                'new_posts': int,
                'error': str (if failed)
            }
        """
        start_time = datetime.now(timezone.utc)
        log_id = None
        
        try:
            logger.info(f"Starting crawl for site: {site_id}")
            
            # 사이트 정보 조회
            site = get_site(site_id)
            if not site:
                logger.error(f"Site not found: {site_id}")
                return {
                    'status': 'failed',
                    'error': 'Site not found'
                }
            
            # 크롤링 로그 생성 (시작)
            log_data = {
                'site_id': site_id,
                'site_name': site['name'],
                'status': 'running',
                'started_at': start_time
            }
            log = create_crawl_log(log_data)
            log_id = log['id']
            
            # RSS 피드 파싱
            logger.info(f"Parsing RSS feed: {site['rss_url']}")
            
            # 마지막 크롤링 시간 이후의 게시물만 가져오기
            last_crawled_at = site.get('last_crawled_at')
            posts = self.rss_service.parse_rss_feed(
                rss_url=site['rss_url'],
                last_post_id=None  # 일단 모든 게시물 가져오기
            )
            
            logger.info(f"Found {len(posts)} posts from RSS feed")
            
            # 새 게시물 필터링 (마지막 크롤링 시간 이후)
            new_posts = []
            if last_crawled_at:
                # last_crawled_at을 timezone-aware로 변환
                if last_crawled_at.tzinfo is None:
                    last_crawled_at = last_crawled_at.replace(tzinfo=timezone.utc)
                
                for post in posts:
                    post_published = post['published']
                    # post published도 timezone-aware로 변환
                    if post_published and post_published.tzinfo is None:
                        post_published = post_published.replace(tzinfo=timezone.utc)
                    
                    if post_published and post_published > last_crawled_at:
                        new_posts.append(post)
            else:
                # 첫 크롤링이면 최근 3개만 처리
                new_posts = posts[:3]
            
            logger.info(f"Found {len(new_posts)} new posts to process")
            
            # 자동 생성 파이프라인 실행
            projects_created = 0
            if new_posts:
                try:
                    from app.services.pipeline_service import AutoGenerationPipeline
                    
                    # 파이프라인 실행 (최대 3개)
                    pipeline = AutoGenerationPipeline(model='gpt-4.1-nano')
                    result = pipeline.generate_multiple(
                        posts=new_posts,
                        site_id=site_id,
                        site_name=site['name'],
                        max_count=3  # 한 번에 최대 3개까지만 생성
                    )
                    
                    projects_created = result['success']
                    logger.info(f"Pipeline result: {projects_created}/{result['total']} projects created")
                    
                except Exception as e:
                    logger.error(f"Pipeline execution failed: {str(e)}")
                    # 파이프라인 실패해도 크롤링은 계속 진행
            
            # 게시물 제목 목록
            post_titles = [post['title'] for post in new_posts[:10]]  # 최대 10개
            
            # 크롤링 완료
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            # 크롤링 로그 업데이트 (완료)
            log_update = {
                'status': 'success',
                'posts_found': len(posts),
                'new_posts': len(new_posts),
                'projects_created': projects_created,
                'completed_at': end_time,
                'duration_seconds': duration,
                'post_titles': post_titles
            }
            update_crawl_log(log_id, log_update)
            
            # 사이트 통계 업데이트
            next_crawl_at = datetime.now(timezone.utc) + timedelta(minutes=site['crawl_interval'])
            site_update = {
                'last_crawled_at': end_time,
                'next_crawl_at': next_crawl_at,
                'total_crawls': site.get('total_crawls', 0) + 1,
                'success_count': site.get('success_count', 0) + 1,
                'total_posts_found': site.get('total_posts_found', 0) + len(new_posts)
            }
            update_site(site_id, site_update)
            
            logger.info(f"Crawl completed for site {site_id}: {len(new_posts)} new posts in {duration:.2f}s")
            
            return {
                'status': 'success',
                'posts_found': len(posts),
                'new_posts': len(new_posts),
                'projects_created': projects_created,
                'duration': duration
            }
            
        except Exception as e:
            logger.error(f"Crawl failed for site {site_id}: {str(e)}")
            
            # 크롤링 로그 업데이트 (실패)
            if log_id:
                end_time = datetime.now(timezone.utc)
                duration = (end_time - start_time).total_seconds()
                log_update = {
                    'status': 'failed',
                    'error_message': str(e),
                    'completed_at': end_time,
                    'duration_seconds': duration
                }
                update_crawl_log(log_id, log_update)
            
            # 사이트 에러 카운트 증가
            try:
                site = get_site(site_id)
                if site:
                    site_update = {
                        'total_crawls': site.get('total_crawls', 0) + 1,
                        'error_count': site.get('error_count', 0) + 1
                    }
                    
                    # 에러가 5회 이상이면 상태를 'error'로 변경
                    if site_update['error_count'] >= 5:
                        site_update['status'] = 'error'
                        logger.warning(f"Site {site_id} marked as error (5+ failures)")
                    
                    update_site(site_id, site_update)
            except:
                pass
            
            return {
                'status': 'failed',
                'error': str(e)
            }


# 전역 크롤러 인스턴스
_crawler_instance: Optional[SiteCrawler] = None


def get_crawler() -> SiteCrawler:
    """
    전역 크롤러 인스턴스 가져오기
    
    Returns:
        SiteCrawler 인스턴스
    """
    global _crawler_instance
    
    if _crawler_instance is None:
        _crawler_instance = SiteCrawler()
    
    return _crawler_instance


def crawl_site_job(site_id: str):
    """
    사이트 크롤링 작업 (스케줄러에서 호출)
    
    Args:
        site_id: 사이트 ID
    """
    try:
        crawler = get_crawler()
        result = crawler.crawl_site(site_id)
        
        if result['status'] == 'success':
            logger.info(f"✅ Crawl job completed: {site_id} ({result['new_posts']} new posts)")
        else:
            logger.error(f"❌ Crawl job failed: {site_id} - {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Crawl job exception for site {site_id}: {str(e)}")
        return {
            'status': 'failed',
            'error': str(e)
        }

