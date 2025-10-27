"""자동 생성 파이프라인 - RSS 게시물 → 카드뉴스 자동 생성"""

from typing import Dict, Optional
import logging
from datetime import datetime

from app.services.scraper import WebScraper
from app.services.summarizer import AISummarizer
from app.services.card_generator import CardNewsGenerator
from app.utils.firebase import create_project, create_sections, update_project

logger = logging.getLogger(__name__)


class AutoGenerationPipeline:
    """RSS 게시물에서 카드뉴스 자동 생성 파이프라인"""
    
    def __init__(self, model: str = "gpt-4.1-nano"):
        self.scraper = WebScraper()
        self.summarizer = AISummarizer(model=model)
        self.card_generator = CardNewsGenerator(model=model)
        self.model = model
    
    def generate_cardnews_from_post(
        self,
        post: Dict,
        site_id: str,
        site_name: str
    ) -> Optional[str]:
        """
        RSS 게시물로부터 카드뉴스 자동 생성
        
        Args:
            post: RSS 게시물 정보
                {
                    'id': str,
                    'title': str,
                    'link': str,
                    'summary': str,
                    'published': datetime,
                    'author': str
                }
            site_id: 사이트 ID
            site_name: 사이트 이름
            
        Returns:
            생성된 프로젝트 ID 또는 None (실패 시)
        """
        try:
            logger.info(f"Starting auto-generation pipeline for post: {post['title']}")
            
            # Step 1: URL 스크래핑
            logger.info(f"Step 1/4: Scraping URL: {post['link']}")
            try:
                scraped_data = self.scraper.scrape_url(post['link'])
                content = scraped_data['content']
                logger.info(f"Scraped {len(content)} characters")
            except Exception as e:
                logger.warning(f"Failed to scrape URL, using RSS summary: {str(e)}")
                # 스크래핑 실패 시 RSS summary 사용
                content = post['summary']
            
            # 내용이 너무 짧으면 건너뛰기
            if len(content.strip()) < 200:
                logger.warning(f"Content too short ({len(content)} chars), skipping")
                return None
            
            # Step 2: 프로젝트 생성 (초안)
            logger.info("Step 2/4: Creating project")
            project_data = {
                'source_type': 'rss',
                'source_content': content,
                'source_site_id': site_id,
                'source_site_name': site_name,
                'model': self.model,
                'card_start_type': 'title',
                'is_auto_generated': True,
                'version': 1
            }
            project = create_project(project_data)
            project_id = project['id']
            logger.info(f"Project created: {project_id}")
            
            # Step 3: AI 요약 생성
            logger.info("Step 3/4: Generating summary")
            try:
                summary_result = self.summarizer.summarize(content, max_length=200)
                
                # 프로젝트 업데이트 (요약)
                update_project(project_id, {
                    'summary': summary_result['summary'],
                    'keywords': summary_result['keywords'],
                    'recommended_card_count': summary_result['card_count'],
                    'status': 'summarized'
                })
                logger.info(f"Summary generated: {len(summary_result['summary'])} chars")
                
            except Exception as e:
                logger.error(f"Failed to generate summary: {str(e)}")
                # 요약 실패 시 프로젝트 삭제
                return None
            
            # Step 4: 카드뉴스 생성
            logger.info("Step 4/4: Generating card news sections")
            try:
                sections = self.card_generator.generate_sections(
                    summary=summary_result['summary'],
                    original_text=content,
                    card_count=summary_result['card_count']
                )
                
                # 섹션 저장
                create_sections(project_id, sections)
                
                # 프로젝트 상태 업데이트 (완료)
                update_project(project_id, {'status': 'completed'})
                
                logger.info(f"✅ Auto-generation completed: {project_id} ({len(sections)} sections)")
                return project_id
                
            except Exception as e:
                logger.error(f"Failed to generate sections: {str(e)}")
                # 섹션 생성 실패 시에도 프로젝트는 유지 (요약 상태)
                return project_id
            
        except Exception as e:
            logger.error(f"Pipeline failed for post {post['title']}: {str(e)}")
            return None
    
    def generate_multiple(
        self,
        posts: list,
        site_id: str,
        site_name: str,
        max_count: int = 5
    ) -> Dict:
        """
        여러 게시물에서 카드뉴스 자동 생성
        
        Args:
            posts: RSS 게시물 목록
            site_id: 사이트 ID
            site_name: 사이트 이름
            max_count: 최대 생성 개수
            
        Returns:
            생성 결과
            {
                'total': int,
                'success': int,
                'failed': int,
                'project_ids': List[str]
            }
        """
        logger.info(f"Starting batch generation for {len(posts)} posts (max: {max_count})")
        
        result = {
            'total': min(len(posts), max_count),
            'success': 0,
            'failed': 0,
            'project_ids': []
        }
        
        for i, post in enumerate(posts[:max_count]):
            logger.info(f"Processing post {i+1}/{result['total']}: {post['title']}")
            
            try:
                project_id = self.generate_cardnews_from_post(post, site_id, site_name)
                
                if project_id:
                    result['success'] += 1
                    result['project_ids'].append(project_id)
                    logger.info(f"✅ Success: {project_id}")
                else:
                    result['failed'] += 1
                    logger.warning(f"❌ Failed: {post['title']}")
                    
            except Exception as e:
                result['failed'] += 1
                logger.error(f"❌ Exception for post {post['title']}: {str(e)}")
        
        logger.info(f"Batch generation completed: {result['success']}/{result['total']} successful")
        return result

