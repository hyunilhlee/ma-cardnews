"""웹 스크래핑 서비스"""

from bs4 import BeautifulSoup
import requests
from newspaper import Article
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class WebScraper:
    """웹 페이지에서 본문 텍스트를 추출하는 서비스"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_url(self, url: str) -> Dict[str, str]:
        """
        URL에서 제목과 본문을 추출
        
        Args:
            url: 스크래핑할 웹 페이지 URL
            
        Returns:
            {
                'title': str,
                'content': str,
                'authors': list,
                'publish_date': str,
                'top_image': str
            }
        """
        try:
            logger.info(f"Scraping URL: {url}")
            # newspaper3k 사용 (뉴스 기사에 최적화)
            # 언어 자동 감지 시도 (한국어 우선, 실패 시 영어)
            article = None
            content = ""
            
            # 먼저 언어 지정 없이 시도
            try:
                article = Article(url)
                article.download()
                article.parse()
                content = article.text or ""
            except:
                pass
            
            # content가 없으면 한국어로 시도
            if not content:
                try:
                    article = Article(url, language='ko')
                    article.download()
                    article.parse()
                    content = article.text or ""
                except:
                    pass
            
            # 여전히 없으면 영어로 시도
            if not content:
                try:
                    article = Article(url, language='en')
                    article.download()
                    article.parse()
                    content = article.text or ""
                except:
                    pass
            
            if not article:
                raise Exception("Failed to parse article with newspaper3k")
            
            result = {
                'title': article.title or "제목 없음",
                'content': content,
                'authors': article.authors or [],
                'publish_date': str(article.publish_date) if article.publish_date else None,
                'top_image': article.top_image or None
            }
            
            logger.info(f"Successfully scraped: {result['title']} ({len(content)} chars)")
            return result
            
        except Exception as e:
            logger.warning(f"newspaper3k failed: {str(e)}, trying BeautifulSoup fallback")
            # Fallback: BeautifulSoup 사용
            return self._fallback_scrape(url)
    
    def _fallback_scrape(self, url: str) -> Dict[str, str]:
        """
        newspaper3k 실패 시 BeautifulSoup으로 스크래핑
        
        Args:
            url: 스크래핑할 웹 페이지 URL
            
        Returns:
            기본 스크래핑 결과
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 제목 추출
            title = soup.find('h1')
            title_text = title.get_text().strip() if title else "제목 없음"
            
            # 본문 추출 (일반적인 article 태그 우선)
            article = soup.find('article')
            if article:
                paragraphs = article.find_all('p')
            else:
                paragraphs = soup.find_all('p')
            
            content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            if not content:
                raise ValueError("본문을 찾을 수 없습니다.")
            
            return {
                'title': title_text,
                'content': content,
                'authors': [],
                'publish_date': None,
                'top_image': None
            }
            
        except Exception as e:
            logger.error(f"Fallback scraping failed: {str(e)}")
            raise ValueError(f"웹 페이지를 스크래핑할 수 없습니다: {str(e)}")

