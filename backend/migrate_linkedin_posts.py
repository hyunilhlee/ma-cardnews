"""
LinkedIn 게시물 재처리 마이그레이션 스크립트

기존 DB의 LinkedIn URL을 가진 RSS 게시물을 찾아서:
1. LinkedIn 전용 스크래핑으로 본문만 추출
2. 한글로 번역
3. DB 업데이트
"""

import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.utils.firebase import get_db, get_all_rss_posts, update_rss_post
from app.services.scraper import WebScraper
import logging
from datetime import datetime
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def is_linkedin_url(url: str) -> bool:
    """LinkedIn URL인지 확인"""
    return 'linkedin.com/posts/' in url or 'linkedin.com/feed/update/' in url


def migrate_linkedin_posts():
    """
    기존 DB의 LinkedIn 게시물 재처리
    """
    logger.info("=" * 80)
    logger.info("LinkedIn 게시물 재처리 마이그레이션 시작")
    logger.info("=" * 80)
    
    try:
        # Firebase 초기화 확인
        db = get_db()
        if db is None:
            logger.error("❌ Firestore not initialized")
            return
        
        logger.info("✅ Firestore connected")
        
        # 모든 RSS 게시물 조회 (limit 없이)
        logger.info("\n📡 Fetching all RSS posts from DB...")
        all_posts = get_all_rss_posts(limit=10000)
        logger.info(f"✅ Found {len(all_posts)} total RSS posts")
        
        # LinkedIn URL 필터링
        linkedin_posts = [post for post in all_posts if is_linkedin_url(post.get('url', ''))]
        logger.info(f"🔍 Found {len(linkedin_posts)} LinkedIn posts")
        
        if not linkedin_posts:
            logger.info("✅ No LinkedIn posts to migrate")
            return
        
        # 통계
        stats = {
            'total': len(linkedin_posts),
            'success': 0,
            'skipped': 0,
            'failed': 0
        }
        
        # WebScraper 초기화
        scraper = WebScraper()
        
        # 각 LinkedIn 게시물 재처리
        logger.info(f"\n🔄 Processing {len(linkedin_posts)} LinkedIn posts...\n")
        
        for idx, post in enumerate(linkedin_posts, 1):
            post_id = post.get('id')
            url = post.get('url')
            title = post.get('title', '')
            
            logger.info(f"[{idx}/{len(linkedin_posts)}] Processing: {title[:50]}...")
            logger.info(f"  URL: {url}")
            
            try:
                # 이미 번역된 게시물인지 확인 (title_original이 있으면 이미 처리됨)
                if post.get('title_original'):
                    logger.info(f"  ⏭️  Already processed (has title_original), skipping")
                    stats['skipped'] += 1
                    continue
                
                # 기존 content 확인
                original_content = post.get('content', '') or post.get('summary', '')
                
                if not original_content or len(original_content) < 10:
                    logger.warning(f"  ⚠️  No content in DB, skipping")
                    stats['skipped'] += 1
                    continue
                
                logger.info(f"  📝 Original content: {original_content[:100]}...")
                
                # 한글로 번역 (scraper의 번역 메서드 사용)
                logger.info(f"  🌐 Translating to Korean...")
                translated_content = scraper._translate_to_korean(original_content)
                
                # 제목도 번역
                logger.info(f"  📰 Translating title...")
                translated_title = scraper._translate_to_korean(title)
                
                logger.info(f"  ✅ Translation completed")
                logger.info(f"     Original title: {title[:50]}...")
                logger.info(f"     Translated title: {translated_title[:50]}...")
                logger.info(f"     Translated content: {translated_content[:100]}...")
                
                # DB 업데이트
                update_data = {
                    'title': translated_title,     # 한글 번역된 제목
                    'title_original': title,       # 원본 제목 보존
                    'content': translated_content, # 한글 번역된 본문
                    'summary': translated_content[:500],  # 요약도 업데이트
                    'updated_at': datetime.now()
                }
                
                update_rss_post(post_id, update_data)
                logger.info(f"  💾 Updated in DB")
                logger.info(f"  ✅ SUCCESS\n")
                
                stats['success'] += 1
                
                # Rate limiting (OpenAI API 호출 제한 방지)
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"  ❌ FAILED: {str(e)}\n")
                stats['failed'] += 1
                continue
        
        # 최종 통계
        logger.info("\n" + "=" * 80)
        logger.info("📊 Migration Statistics")
        logger.info("=" * 80)
        logger.info(f"Total LinkedIn posts: {stats['total']}")
        logger.info(f"✅ Successfully migrated: {stats['success']}")
        logger.info(f"⏭️  Skipped (already processed): {stats['skipped']}")
        logger.info(f"❌ Failed: {stats['failed']}")
        logger.info("=" * 80)
        
        if stats['success'] > 0:
            logger.info("\n✅ Migration completed successfully!")
            logger.info("🔄 RSS Library will now show translated LinkedIn posts")
        else:
            logger.info("\n⚠️  No posts were migrated")
        
    except Exception as e:
        logger.error(f"\n❌ Migration failed: {str(e)}")
        raise


if __name__ == "__main__":
    logger.info("Starting LinkedIn posts migration...\n")
    
    try:
        migrate_linkedin_posts()
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Migration interrupted by user")
    except Exception as e:
        logger.error(f"\n\n❌ Fatal error: {str(e)}")
        sys.exit(1)

