"""
기존 RSS 게시물 한글 번역 및 키워드 추출 마이그레이션 스크립트

- 모든 기존 RSS 게시물 조회
- 제목 한글 번역 (영문인 경우)
- 요약 생성 (8-12문장, 한글)
- 키워드 추출
- DB 업데이트
"""

import sys
import os
import re
import logging
from datetime import datetime

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.firebase import get_all_rss_posts, update_rss_post
from app.services.summarizer import AISummarizer
from app.services.scraper import WebScraper
from openai import OpenAI

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def translate_title_to_korean(title: str) -> str:
    """제목을 한글로 번역 (영문인 경우)"""
    # 영문이 포함되어 있는지 확인
    if not re.search(r'[a-zA-Z]{3,}', title):
        logger.info(f"Title already in Korean: {title}")
        return title
    
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model='gpt-4.1-nano',
            messages=[
                {"role": "system", "content": "당신은 전문 번역가입니다. 제목을 간결하고 자연스러운 한글로 번역해주세요."},
                {"role": "user", "content": f"다음 제목을 한글로 번역해주세요:\n\n{title}"}
            ],
            temperature=0.3,
            max_tokens=100
        )
        translated = response.choices[0].message.content.strip()
        logger.info(f"Translated: {title} → {translated}")
        return translated
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        return title


def migrate_rss_posts():
    """기존 RSS 게시물 마이그레이션"""
    logger.info("Starting RSS posts migration...")
    
    # 모든 RSS 게시물 조회
    all_posts = get_all_rss_posts()
    logger.info(f"Found {len(all_posts)} RSS posts")
    
    if not all_posts:
        logger.warning("No RSS posts found in DB")
        return
    
    # AI 도구 초기화
    summarizer = AISummarizer(model='gpt-4.1-nano')
    scraper = WebScraper()
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, post in enumerate(all_posts, 1):
        try:
            post_id = post['id']
            title = post.get('title', '')
            url = post.get('url', '')
            
            logger.info(f"\n[{i}/{len(all_posts)}] Processing: {title[:50]}...")
            
            # 이미 번역/키워드가 있는지 확인
            has_korean_title = post.get('title_original') is not None
            has_keywords = post.get('keywords') and len(post.get('keywords', [])) > 0
            has_ai_summary = post.get('summary') and len(post.get('summary', '')) > 100
            
            if has_korean_title and has_keywords and has_ai_summary:
                logger.info(f"  ✓ Already migrated, skipping...")
                skip_count += 1
                continue
            
            # 1. 콘텐츠 가져오기
            content = post.get('content', '')
            
            # content가 짧으면 URL 스크래핑
            if len(content) < 200 and url:
                try:
                    logger.info(f"  📄 Scraping content from URL...")
                    scraped_data = scraper.scrape_url(url)
                    content = scraped_data.get('content', content)
                    logger.info(f"  ✓ Scraped {len(content)} characters")
                except Exception as e:
                    logger.warning(f"  ⚠ Scraping failed: {str(e)}")
            
            # 업데이트할 데이터
            update_data = {}
            
            # 2. 제목 번역 (영문인 경우)
            if not has_korean_title:
                logger.info(f"  🌐 Translating title...")
                title_kr = translate_title_to_korean(title)
                if title_kr != title:
                    update_data['title'] = title_kr
                    update_data['title_original'] = title
                    logger.info(f"  ✓ Title translated")
                else:
                    logger.info(f"  ✓ Title already in Korean")
            
            # 3. AI 요약 및 키워드 추출
            if content and len(content) >= 100:
                logger.info(f"  ✨ Generating AI summary and keywords...")
                try:
                    summary_result = summarizer.summarize(
                        content,
                        max_length=None,
                        additional_instructions="적절한 길이로 요약해주세요. 8-12문장 정도로 작성하세요. 모든 내용을 한글로 번역해서 작성해주세요."
                    )
                    
                    ai_summary = summary_result.get('summary', '')
                    keywords = summary_result.get('keywords', [])
                    
                    if ai_summary:
                        update_data['summary'] = ai_summary
                        logger.info(f"  ✓ Summary generated ({len(ai_summary)} chars)")
                    
                    if keywords:
                        update_data['keywords'] = keywords
                        logger.info(f"  ✓ Keywords extracted: {keywords}")
                    
                except Exception as e:
                    logger.error(f"  ✗ AI processing failed: {str(e)}")
            else:
                logger.warning(f"  ⚠ Content too short ({len(content)} chars), skipping AI processing")
            
            # 4. DB 업데이트
            if update_data:
                logger.info(f"  💾 Updating DB...")
                update_rss_post(post_id, update_data)
                success_count += 1
                logger.info(f"  ✅ Successfully updated!")
            else:
                logger.info(f"  ℹ️ No updates needed")
                skip_count += 1
            
        except Exception as e:
            logger.error(f"  ✗ Error processing post: {str(e)}")
            error_count += 1
            continue
    
    # 결과 요약
    logger.info("\n" + "="*60)
    logger.info("Migration completed!")
    logger.info(f"Total: {len(all_posts)} posts")
    logger.info(f"✅ Success: {success_count}")
    logger.info(f"⏭️  Skipped: {skip_count}")
    logger.info(f"✗ Errors: {error_count}")
    logger.info("="*60)


if __name__ == "__main__":
    logger.info("RSS Posts Migration Script")
    logger.info("="*60)
    
    # 확인 메시지
    logger.info("\n⚠️  WARNING: This will update all RSS posts in the database.")
    logger.info("   - Translate titles to Korean")
    logger.info("   - Generate AI summaries")
    logger.info("   - Extract keywords")
    logger.info("\nThis may take several minutes and consume OpenAI API credits.\n")
    
    # 자동 실행 (확인 건너뛰기)
    migrate_rss_posts()

