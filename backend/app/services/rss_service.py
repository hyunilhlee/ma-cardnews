"""RSS 피드 파싱 서비스"""

import feedparser
import logging
from typing import List, Dict, Optional
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RSSService:
    """RSS 피드 파싱 및 검증 서비스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def validate_rss_url(self, rss_url: str) -> Dict[str, any]:
        """
        RSS URL 검증
        
        Args:
            rss_url: RSS 피드 URL
            
        Returns:
            {
                'valid': bool,
                'title': str,
                'description': str,
                'error': str (if not valid)
            }
        """
        try:
            logger.info(f"Validating RSS URL: {rss_url}")
            
            # URL 형식 검증
            parsed = urlparse(rss_url)
            if not parsed.scheme or not parsed.netloc:
                return {
                    'valid': False,
                    'error': 'Invalid URL format'
                }
            
            # RSS 피드 파싱
            feed = feedparser.parse(rss_url)
            
            # 파싱 에러 확인
            if feed.bozo and hasattr(feed, 'bozo_exception'):
                logger.warning(f"RSS parsing warning: {feed.bozo_exception}")
            
            # 피드가 비어있는지 확인
            if not feed.entries:
                return {
                    'valid': False,
                    'error': 'No entries found in RSS feed'
                }
            
            # 성공
            return {
                'valid': True,
                'title': feed.feed.get('title', 'Unknown'),
                'description': feed.feed.get('description', ''),
                'total_entries': len(feed.entries),
                'link': feed.feed.get('link', '')
            }
            
        except Exception as e:
            logger.error(f"RSS validation failed for {rss_url}: {str(e)}")
            return {
                'valid': False,
                'error': str(e)
            }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def parse_rss_feed(self, rss_url: str, last_post_id: Optional[str] = None) -> List[Dict]:
        """
        RSS 피드 파싱 및 새 게시물 추출
        
        Args:
            rss_url: RSS 피드 URL
            last_post_id: 마지막으로 처리한 게시물 ID (link 또는 guid)
            
        Returns:
            List of posts:
            [
                {
                    'id': str (link or guid),
                    'title': str,
                    'link': str,
                    'summary': str,
                    'published': datetime,
                    'author': str
                }
            ]
        """
        try:
            logger.info(f"Parsing RSS feed: {rss_url}")
            
            # RSS 피드 파싱
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                logger.warning(f"No entries found in {rss_url}")
                return []
            
            posts = []
            found_last_post = False
            
            for entry in feed.entries:
                # 게시물 ID (link 또는 guid 사용)
                post_id = entry.get('link') or entry.get('id') or entry.get('guid')
                
                if not post_id:
                    logger.warning(f"Skipping entry without ID: {entry.get('title')}")
                    continue
                
                # 마지막 처리한 게시물까지 도달하면 중단
                if last_post_id and post_id == last_post_id:
                    found_last_post = True
                    break
                
                # 게시물 데이터 추출
                post = self._extract_post_data(entry)
                posts.append(post)
            
            logger.info(f"Found {len(posts)} new posts from {rss_url}")
            
            if last_post_id and not found_last_post:
                logger.warning(f"Last post ID not found in feed, returning all posts")
            
            return posts
            
        except Exception as e:
            logger.error(f"RSS parsing failed for {rss_url}: {str(e)}")
            raise
    
    def _extract_post_data(self, entry: Dict) -> Dict:
        """
        RSS 엔트리에서 게시물 데이터 추출
        
        Args:
            entry: feedparser entry
            
        Returns:
            Post data dictionary
        """
        # ID
        post_id = entry.get('link') or entry.get('id') or entry.get('guid')
        
        # 제목
        title = entry.get('title', 'No Title')
        
        # 링크
        link = entry.get('link', '')
        
        # 요약/내용 - content와 summary 모두 추출
        summary = ''
        content = ''
        
        # 먼저 content 확인 (더 상세한 내용)
        if 'content' in entry and entry.content:
            content = entry.content[0].get('value', '')
        
        # summary 또는 description
        if 'summary' in entry:
            summary = entry.summary
        elif 'description' in entry:
            summary = entry.description
        
        # content가 없으면 summary를 content로 사용
        if not content:
            content = summary
        
        # HTML 태그 제거
        summary = self._strip_html_tags(summary)
        content = self._strip_html_tags(content)
        
        # 발행일
        published = None
        if 'published_parsed' in entry and entry.published_parsed:
            try:
                published = datetime(*entry.published_parsed[:6])
            except:
                pass
        
        if not published and 'updated_parsed' in entry and entry.updated_parsed:
            try:
                published = datetime(*entry.updated_parsed[:6])
            except:
                pass
        
        if not published:
            published = datetime.now()
        
        # 저자
        author = entry.get('author', 'Unknown')
        
        return {
            'id': post_id,
            'title': title,
            'link': link,
            'summary': summary[:500],  # 500자로 제한
            'content': content,  # 전체 내용 (제한 없음)
            'published': published,
            'author': author
        }
    
    def _strip_html_tags(self, text: str) -> str:
        """
        HTML 태그 제거 (간단한 처리)
        
        Args:
            text: HTML 포함 텍스트
            
        Returns:
            태그가 제거된 텍스트
        """
        import re
        
        # HTML 태그 제거
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', text)
        
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def get_feed_info(self, rss_url: str) -> Dict:
        """
        RSS 피드 기본 정보 조회
        
        Args:
            rss_url: RSS 피드 URL
            
        Returns:
            Feed info dictionary
        """
        try:
            feed = feedparser.parse(rss_url)
            
            return {
                'title': feed.feed.get('title', 'Unknown'),
                'description': feed.feed.get('description', ''),
                'link': feed.feed.get('link', ''),
                'language': feed.feed.get('language', 'en'),
                'updated': feed.feed.get('updated', ''),
                'total_entries': len(feed.entries)
            }
            
        except Exception as e:
            logger.error(f"Failed to get feed info for {rss_url}: {str(e)}")
            return {}

