"""RSS Library 서비스 - 통합 피드 제공"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta, timezone
import hashlib
import logging

from app.services.rss_service import RSSService
from app.utils.firebase import get_all_projects, get_all_sites

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
            
            # 2. 실시간 RSS 피드 가져오기 (캐시 활용)
            rss_posts = await self._get_rss_posts_feed(site_id)
            logger.info(f"Found {len(rss_posts)} posts from RSS feeds")
            
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
    
    async def _get_rss_posts_feed(
        self,
        site_id: Optional[str]
    ) -> List[Dict]:
        """실시간 RSS 피드에서 게시물 조회 (캐시 활용)"""
        try:
            # 캐시 확인
            cache_key = f"rss_feed_{site_id or 'all'}"
            if cache_key in self.cache:
                cached_data, cached_time = self.cache[cache_key]
                if (datetime.now(timezone.utc) - cached_time).total_seconds() < self.cache_ttl:
                    logger.info(f"Using cached RSS feed for {cache_key}")
                    return cached_data
            
            # RSS 피드 파싱
            sites = get_all_sites()
            if site_id:
                sites = [s for s in sites if s['id'] == site_id]
            
            # active 사이트만
            sites = [s for s in sites if s.get('status') == 'active']
            
            feed_items = []
            existing_urls = set()  # 중복 확인용
            
            for site in sites:
                try:
                    logger.info(f"Parsing RSS feed for site: {site['name']}")
                    posts = self.rss_service.parse_rss_feed(
                        rss_url=site['rss_url'],
                        last_post_id=None
                    )
                    
                    for post in posts[:50]:  # 최대 50개만
                        post_url = post['link']
                        
                        # URL 중복 체크
                        if post_url in existing_urls:
                            continue
                        existing_urls.add(post_url)
                        
                        # 이미 프로젝트가 있는지 확인 (간단히 URL로)
                        # 실제로는 Firestore 쿼리 필요하지만, 성능을 위해 생략
                        # (나중에 merge에서 중복 제거됨)
                        
                        post_id = self._generate_post_id(post_url)
                        
                        feed_items.append({
                            'id': post_id,
                            'type': 'rss_post',
                            'title': post['title'],
                            'source': {
                                'site_id': site['id'],
                                'site_name': site['name'],
                                'site_url': site['url']
                            },
                            'keywords': [],  # RSS에서는 키워드 없음
                            'summary': post.get('summary', '')[:200],
                            'published_at': post['published'],
                            'url': post_url,
                            'has_cardnews': False,
                            'project_id': None,
                            'status': None,
                            'is_new': self._is_new(post['published'])
                        })
                        
                except Exception as e:
                    logger.error(f"Failed to parse RSS feed for site {site['name']}: {str(e)}")
                    continue
            
            # 캐시 저장
            self.cache[cache_key] = (feed_items, datetime.now(timezone.utc))
            
            return feed_items
            
        except Exception as e:
            logger.error(f"Failed to get RSS posts feed: {str(e)}")
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

