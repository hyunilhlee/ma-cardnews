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
            
            # LinkedIn 게시물인 경우 전용 스크래핑
            if 'linkedin.com/posts/' in url or 'linkedin.com/feed/update/' in url:
                logger.info("Detected LinkedIn post, using specialized scraper")
                return self._scrape_linkedin_post(url)
            
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
    
    def _scrape_linkedin_post(self, url: str) -> Dict[str, str]:
        """
        LinkedIn 게시물 전용 스크래핑
        - 게시물 본문만 추출 (댓글 제외)
        - 한글로 자동 번역
        
        Args:
            url: LinkedIn 게시물 URL
            
        Returns:
            {
                'title': str,       # 작성자 이름 + "LinkedIn 게시물"
                'content': str,     # 게시물 본문 (한글 번역)
                'authors': list,
                'publish_date': None,
                'top_image': None
            }
        """
        try:
            logger.info(f"Scraping LinkedIn post: {url}")
            
            # LinkedIn 페이지 요청
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 게시물 본문 추출 (댓글 제외)
            post_content = ""
            
            # 방법 1: update-components-text 클래스 찾기
            content_div = soup.find('div', class_='update-components-text')
            if content_div:
                # span 태그들에서 텍스트 추출
                spans = content_div.find_all('span', recursive=True)
                post_content = ' '.join([span.get_text(strip=True) for span in spans if span.get_text(strip=True)])
            
            # 방법 2: update-v2__commentary 클래스 찾기
            if not post_content:
                content_div = soup.find('div', class_=lambda x: x and 'update-v2__commentary' in x)
                if content_div:
                    post_content = content_div.get_text(strip=True)
            
            # 방법 3: 일반적인 게시물 컨테이너 찾기
            if not post_content:
                content_div = soup.find('div', class_=lambda x: x and 'feed-shared-update-v2__description' in x)
                if content_div:
                    post_content = content_div.get_text(strip=True)
            
            if not post_content:
                raise ValueError("LinkedIn 게시물 본문을 찾을 수 없습니다.")
            
            logger.info(f"Extracted LinkedIn post content: {post_content[:100]}...")
            
            # 작성자 이름 추출
            author_name = "LinkedIn User"
            try:
                # 작성자 이름 추출 시도
                author_div = soup.find('span', class_='update-components-actor__name')
                if author_div:
                    author_name = author_div.get_text(strip=True)
                else:
                    # 대체 방법
                    author_link = soup.find('a', class_=lambda x: x and 'app-aware-link' in x)
                    if author_link:
                        author_name = author_link.get_text(strip=True)
            except Exception as e:
                logger.warning(f"Failed to extract author name: {str(e)}")
            
            # 한글로 번역
            translated_content = self._translate_to_korean(post_content)
            
            result = {
                'title': f"{author_name}의 LinkedIn 게시물",
                'content': translated_content,
                'authors': [author_name],
                'publish_date': None,
                'top_image': None
            }
            
            logger.info(f"Successfully scraped LinkedIn post by {author_name}")
            return result
            
        except Exception as e:
            logger.error(f"LinkedIn post scraping failed: {str(e)}")
            raise ValueError(f"LinkedIn 게시물을 스크래핑할 수 없습니다: {str(e)}")
    
    def _translate_to_korean(self, text: str) -> str:
        """
        텍스트를 한글로 번역
        
        Args:
            text: 번역할 텍스트
            
        Returns:
            번역된 한글 텍스트
        """
        try:
            # 이미 한글이 많으면 번역 생략
            import re
            korean_chars = len(re.findall(r'[가-힣]', text))
            total_chars = len(text.replace(' ', ''))
            
            if total_chars > 0 and korean_chars / total_chars > 0.3:
                logger.info("Text is already in Korean (>30%), skipping translation")
                return text
            
            # OpenAI로 번역
            from openai import OpenAI
            from app.config import settings
            
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model='gpt-4.1-nano',
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 전문 번역가입니다. 주어진 텍스트를 자연스러운 한글로 번역해주세요. 원문의 의미와 뉘앙스를 정확히 전달하되, 한국어로 읽기 편하게 작성하세요."
                    },
                    {
                        "role": "user",
                        "content": f"다음 텍스트를 한글로 번역해주세요:\n\n{text}"
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            translated = response.choices[0].message.content.strip()
            logger.info(f"Translation completed: {len(text)} chars -> {len(translated)} chars")
            
            return translated
            
        except Exception as e:
            logger.warning(f"Translation failed: {str(e)}, returning original text")
            return text

