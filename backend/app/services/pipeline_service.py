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
                content = scraped_data.get('main_content', '') or scraped_data.get('content', '')
                logger.info(f"Scraped {len(content)} characters")
                
                # 스크래핑 실패 시 RSS content 또는 summary 사용
                if len(content.strip()) < 200:
                    logger.warning(f"Scraped content too short, using RSS content/summary")
                    content = post.get('content', '') or post.get('summary', '')
                    
            except Exception as e:
                logger.warning(f"Failed to scrape URL, using RSS content/summary: {str(e)}")
                # 스크래핑 실패 시 RSS content 또는 summary 사용
                content = post.get('content', '') or post.get('summary', '')
            
            # Step 2: 프로젝트 생성 (모든 피드 보존)
            logger.info("Step 2/4: Creating project")
            
            # 내용 길이에 관계없이 프로젝트 생성 (최소 10자 이상만)
            if len(content.strip()) < 10:
                logger.warning(f"Content too short ({len(content)} chars), skipping completely")
                return None
            
            project_data = {
                'title': post.get('title', 'Untitled'),
                'source_type': 'rss',
                'source_url': post.get('link', ''),
                'source_text': content,
                'source_site_id': site_id,
                'source_site_name': site_name,
                'model': self.model,
                'card_start_type': 'title',
                'is_auto_generated': True,
                'status': 'draft',
                'version': 1,
                'original_published_at': post.get('published')
            }
            project = create_project(project_data)
            project_id = project['id']
            logger.info(f"Project created: {project_id}")
            
            # 내용이 너무 짧으면 요약/생성 스킵하고 draft로 유지
            if len(content.strip()) < 200:
                logger.warning(f"Content too short ({len(content)} chars), keeping as draft for manual review")
                update_project(project_id, {
                    'status': 'draft',
                    'summary': f"⚠️ 내용이 짧아 자동 생성을 건너뛰었습니다. ({len(content)}자)\n\n수동으로 완성해주세요.",
                    'last_error': f'Content too short: {len(content)} chars'
                })
                return project_id  # draft 상태로 유지
            
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
                # 요약 실패 시에도 프로젝트 유지 (draft 상태)
                update_project(project_id, {
                    'status': 'draft',
                    'summary': f"⚠️ 요약 생성에 실패했습니다.\n\n오류: {str(e)}\n\n수동으로 완성해주세요.",
                    'last_error': f'Summary generation failed: {str(e)}'
                })
                logger.warning(f"Summary failed, keeping project {project_id} as draft")
                return project_id  # draft 상태로 유지
            
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
                update_project(project_id, {
                    'status': 'completed',
                    'last_error': None  # 에러 초기화
                })
                
                logger.info(f"✅ Auto-generation completed: {project_id} ({len(sections)} sections)")
                return project_id
                
            except Exception as e:
                logger.error(f"Failed to generate sections: {str(e)}")
                # 섹션 생성 실패 시에도 프로젝트 유지 (summarized 상태)
                # 요약까지는 성공했으므로 사용자가 수동으로 카드뉴스 생성 가능
                update_project(project_id, {
                    'status': 'summarized',
                    'last_error': f'Card generation failed: {str(e)}'
                })
                logger.warning(f"Card generation failed, keeping project {project_id} as summarized (요약까지 완료)")
                return project_id  # summarized 상태로 유지
            
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

