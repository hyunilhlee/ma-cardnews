"""RSS 피드 파서 테스트 스크립트"""

import sys
import os

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.rss_service import RSSService
from datetime import datetime


def test_microsoft_rss_feeds():
    """Microsoft RSS 피드 3개 테스트"""
    
    rss_service = RSSService()
    
    # 테스트할 RSS 피드 목록
    test_feeds = [
        {
            'name': 'Microsoft Blogs',
            'url': 'https://blogs.microsoft.com/',
            'rss_url': 'https://blogs.microsoft.com/feed/'
        },
        {
            'name': 'Microsoft News Source',
            'url': 'https://news.microsoft.com/source/',
            'rss_url': 'https://news.microsoft.com/source/feed'
        },
        {
            'name': 'Microsoft Security',
            'url': 'https://www.microsoft.com/en-us/security/blog/',
            'rss_url': 'https://www.microsoft.com/en-us/security/blog/feed/'
        }
    ]
    
    print("=" * 80)
    print("🧪 Microsoft RSS 피드 테스트 시작")
    print("=" * 80)
    print()
    
    results = []
    
    for feed_info in test_feeds:
        print(f"📡 테스트: {feed_info['name']}")
        print(f"   URL: {feed_info['url']}")
        print(f"   RSS: {feed_info['rss_url']}")
        print()
        
        # 1. RSS URL 검증
        print("   ⏳ Step 1: RSS URL 검증 중...")
        validation = rss_service.validate_rss_url(feed_info['rss_url'])
        
        if validation['valid']:
            print(f"   ✅ 검증 성공!")
            print(f"      제목: {validation['title']}")
            print(f"      총 게시물: {validation['total_entries']}개")
            
            # 2. RSS 피드 파싱
            print()
            print("   ⏳ Step 2: RSS 피드 파싱 중...")
            posts = rss_service.parse_rss_feed(feed_info['rss_url'])
            
            if posts:
                print(f"   ✅ 파싱 성공! {len(posts)}개 게시물 발견")
                print()
                print("   📰 최근 게시물 3개:")
                for i, post in enumerate(posts[:3], 1):
                    print(f"      {i}. {post['title']}")
                    print(f"         링크: {post['link']}")
                    print(f"         발행일: {post['published'].strftime('%Y-%m-%d %H:%M')}")
                    print(f"         요약: {post['summary'][:100]}...")
                    print()
                
                results.append({
                    'name': feed_info['name'],
                    'status': 'success',
                    'posts_count': len(posts)
                })
            else:
                print(f"   ⚠️  게시물을 찾을 수 없습니다.")
                results.append({
                    'name': feed_info['name'],
                    'status': 'no_posts',
                    'posts_count': 0
                })
        else:
            print(f"   ❌ 검증 실패: {validation['error']}")
            results.append({
                'name': feed_info['name'],
                'status': 'failed',
                'error': validation['error']
            })
        
        print("-" * 80)
        print()
    
    # 결과 요약
    print("=" * 80)
    print("📊 테스트 결과 요약")
    print("=" * 80)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    total_count = len(results)
    
    print(f"✅ 성공: {success_count}/{total_count}")
    print()
    
    for result in results:
        status_icon = "✅" if result['status'] == 'success' else "❌"
        print(f"{status_icon} {result['name']}")
        if result['status'] == 'success':
            print(f"   게시물: {result['posts_count']}개")
        elif result['status'] == 'failed':
            print(f"   에러: {result.get('error', 'Unknown')}")
        print()
    
    print("=" * 80)


if __name__ == "__main__":
    test_microsoft_rss_feeds()

