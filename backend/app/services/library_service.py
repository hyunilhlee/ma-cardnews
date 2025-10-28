"""RSS Library 서비스 - 통합 피드 제공"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta, timezone
import hashlib
import logging

from app.services.rss_service import RSSService
from app.utils.firebase import get_all_projects, get_all_sites, get_all_rss_posts

logger = logging.getLogger(__name__)


class LibraryService:
    """RSS Library 통합 피드 서비스"""
    
    def __init__(self):
        self.rss_service = RSSService()
        self.cache = {}  # 메모리 캐시 (1시간)
        self.cache_ttl = 3600
    
    async def get_feed(
        self,
        site_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        keyword: Optional[str] = None,
        year_month: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict:
        """
        통합 RSS 피드 조회
        
        Args:
            site_id: 특정 사이트만 조회 (None이면 전체)
            start_date: 시작 날짜
            end_date: 종료 날짜
            keyword: 키워드 검색
            year_month: 연월 필터 (YYYY-MM 형식)
            page: 페이지 번호
            page_size: 페이지 크기
            
        Returns:
            {
                'total': int,
                'page': int,
                'page_size': int,
                'items': List[FeedItem]
            }
        """
        try:
            logger.info(f"Getting library feed (site_id={site_id}, keyword={keyword}, page={page})")
            
            # 1. Firestore에서 RSS 프로젝트 가져오기
            projects = self._get_projects_feed(site_id, start_date, end_date)
            logger.info(f"Found {len(projects)} projects from Firestore")
            
            # 2. DB에 저장된 RSS 게시물 가져오기
            rss_posts = self._get_rss_posts_from_db(site_id, start_date, end_date, year_month)
            logger.info(f"Found {len(rss_posts)} posts from DB")
            
            # 3. 통합 및 중복 제거
            combined = self._merge_feeds(projects, rss_posts)
            logger.info(f"Combined total: {len(combined)} items")
            
            # 4. 필터링
            filtered = self._apply_filters(combined, keyword, start_date, end_date)
            logger.info(f"Filtered: {len(filtered)} items")
            
            # 5. 정렬 (최신순)
            sorted_feed = sorted(
                filtered,
                key=lambda x: x['published_at'] or datetime.min.replace(tzinfo=timezone.utc),
                reverse=True
            )
            
            # 6. 페이지네이션
            total = len(sorted_feed)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            items = sorted_feed[start_idx:end_idx]
            
            return {
                'total': total,
                'page': page,
                'page_size': page_size,
                'items': items
            }
            
        except Exception as e:
            logger.error(f"Failed to get library feed: {str(e)}", exc_info=True)
            return {
                'total': 0,
                'page': page,
                'page_size': page_size,
                'items': []
            }
    
    def _get_projects_feed(
        self,
        site_id: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Dict]:
        """Firestore에서 RSS 프로젝트 조회"""
        try:
            # Firestore 쿼리 (source_type='rss')
            all_projects = get_all_projects(limit=1000)
            
            # RSS 타입만 필터링
            projects = [p for p in all_projects if p.get('source_type') == 'rss']
            
            # 사이트 필터링
            if site_id:
                projects = [p for p in projects if p.get('source_site_id') == site_id]
            
            # FeedItem 형식으로 변환
            feed_items = []
            for project in projects:
                published_at = project.get('original_published_at') or project.get('created_at')
                
                # 날짜 필터링
                if start_date and published_at and published_at < start_date:
                    continue
                if end_date and published_at and published_at > end_date:
                    continue
                
                feed_items.append({
                    'id': project['id'],
                    'type': 'project',
                    'title': project.get('title') or 'Untitled',
                    'source': {
                        'site_id': project.get('source_site_id'),
                        'site_name': project.get('source_site_name') or 'Unknown',
                        'site_url': project.get('source_url') or ''
                    },
                    'keywords': project.get('keywords') or [],
                    'summary': project.get('summary') or '',
                    'published_at': published_at,
                    'url': project.get('source_url') or '',
                    'has_cardnews': True,
                    'project_id': project['id'],
                    'status': project.get('status', 'draft'),
                    'is_new': self._is_new(project.get('created_at'))
                })
            
            return feed_items
            
        except Exception as e:
            logger.error(f"Failed to get projects feed: {str(e)}")
            return []
    
    def _get_rss_posts_from_db(
        self,
        site_id: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        year_month: Optional[str]
    ) -> List[Dict]:
        """DB에 저장된 RSS 게시물 조회"""
        try:
            # Firestore에서 RSS 게시물 조회
            rss_posts = get_all_rss_posts(
                site_id=site_id,
                start_date=start_date,
                end_date=end_date,
                year_month=year_month,
                limit=1000
            )
            
            # FeedItem 형식으로 변환
            feed_items = []
            for post in rss_posts:
                feed_items.append({
                    'id': post['id'],
                    'type': 'rss_post',
                    'title': post['title'],
                    'source': {
                        'site_id': post['site_id'],
                        'site_name': post['site_name'],
                        'site_url': ''
                    },
                    'keywords': [],  # RSS 게시물은 키워드 없음
                    'summary': post.get('summary', '')[:200],
                    'published_at': post['published_at'],
                    'url': post['url'],
                    'has_cardnews': post.get('has_cardnews', False),
                    'project_id': post.get('project_id'),
                    'status': None,
                    'is_new': self._is_new(post.get('crawled_at'))
                })
            
            return feed_items
            
        except Exception as e:
            logger.error(f"Failed to get RSS posts from DB: {str(e)}")
            return []
    
    def _merge_feeds(
        self,
        projects: List[Dict],
        rss_posts: List[Dict]
    ) -> List[Dict]:
        """두 피드를 병합하고 중복 제거"""
        # URL 기반으로 중복 제거
        seen_urls = set()
        merged = []
        
        # 프로젝트 우선 (이미 생성된 것)
        for item in projects:
            url = item['url']
            if url and url not in seen_urls:
                merged.append(item)
                seen_urls.add(url)
        
        # RSS 게시물 추가 (프로젝트에 없는 것만)
        for item in rss_posts:
            url = item['url']
            if url and url not in seen_urls:
                merged.append(item)
                seen_urls.add(url)
        
        return merged
    
    def _apply_filters(
        self,
        items: List[Dict],
        keyword: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Dict]:
        """필터 적용"""
        filtered = items
        
        # 키워드 필터
        if keyword:
            keyword_lower = keyword.lower()
            filtered = []
            
            for item in items:
                # 제목, 요약, 키워드에서 검색
                if (keyword_lower in item['title'].lower() or
                    keyword_lower in item['summary'].lower() or
                    any(keyword_lower in k.lower() for k in item['keywords'])):
                    filtered.append(item)
        
        # 날짜 필터는 이미 _get_projects_feed에서 적용됨
        
        return filtered
    
    def _is_new(self, published_at: Optional[datetime]) -> bool:
        """24시간 이내 게시물인지 확인"""
        if not published_at:
            return False
        
        # timezone-aware로 변환
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        return (now - published_at).total_seconds() < 86400
    
    def _generate_post_id(self, url: str) -> str:
        """URL을 해시하여 게시물 ID 생성"""
        return hashlib.md5(url.encode()).hexdigest()


# 싱글톤 인스턴스
_library_service: Optional[LibraryService] = None

def get_library_service() -> LibraryService:
    """LibraryService 인스턴스 가져오기 (싱글톤)"""
    global _library_service
    if _library_service is None:
        _library_service = LibraryService()
    return _library_service

