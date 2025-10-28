# Phase 2.5 개발 정의서 - RSS Library & 최적화

**프로젝트**: CardNews AI Generator  
**Phase**: Phase 2.5 (RSS Library & Optimization)  
**기간**: 2025-10-28 (1일)  
**상태**: ✅ 완료
**우선순위**: RSS Library (신규 기능) + 사용자 경험 개선

---

## 📋 개요

Phase 2 완료 후, 사용자 경험을 개선하고 RSS 콘텐츠를 더 효과적으로 관리하기 위한 단기 개선 프로젝트입니다.

### 핵심 목표 (모두 달성! ✅)
1. ✅ **RSS Library 구축**: 모든 RSS 게시물을 시간순으로 통합 조회
2. ✅ **자동 AI 처리**: RSS 크롤링 시 자동 번역, 요약, 키워드 추출
3. ✅ **UX 개선**: 카드뉴스 생성 로딩 페이지, Undo 기능
4. ✅ **한글 생성 강화**: 모든 카드뉴스를 한글로 생성

### 범위
- **신규 기능**: RSS Library (메인 페이지 4번째 메뉴)
- **개선 작업**: 자동 AI 처리, 한글 번역, UX 개선
- **완료된 기능**: RSS Posts 저장, Library 페이지, 로딩 페이지, Undo, 한글 생성

---

## 🆕 신규 기능: RSS Library

### 1. 기능 설명

#### 개념
등록된 모든 RSS 사이트의 게시물을 **하나의 통합 피드**로 제공하여, 사용자가 최신 콘텐츠를 한눈에 파악할 수 있도록 합니다.

#### 사용 시나리오
```
1. 사용자가 메인 페이지에서 "RSS Library" 메뉴 클릭
2. 등록된 모든 RSS 사이트의 게시물이 최신순으로 표시됨
   (Microsoft Blogs, Microsoft Security, Microsoft News 등)
3. 각 게시물은 카드 형태로 표시
4. 카드 클릭 시 상세 정보 확인 또는 카드뉴스 생성
5. 필터링 옵션: 사이트별, 날짜별, 키워드별
```

---

### 2. UI/UX 디자인

#### 메인 페이지 메뉴 구조 (4개 → 5개)

```
┌─────────────────────────────────────────────────────────┐
│ CardNews AI Generator                    [로그인] [설정]│
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [1. RSS 사이트 설정]  [2. 수동 생성]  [3. 저장된 프로젝트]  │
│                                                          │
│  ⭐ [4. RSS Library] ⭐  (신규!)                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### RSS Library 페이지 레이아웃

```
┌─────────────────────────────────────────────────────────┐
│ RSS Library                          [필터] [새로고침]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 필터:                                                    │
│ [전체 사이트 ▼] [전체 날짜 ▼] [키워드 검색...]          │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 📰 Microsoft Announces AI Innovations          [>] │ │
│ │                                                     │ │
│ │ 📍 Microsoft Blogs                                  │ │
│ │ 🏷️  #AI #Innovation #Microsoft                     │ │
│ │ 📅 2025-10-28 15:30                                 │ │
│ │                                                     │ │
│ │ Microsoft unveils groundbreaking AI tools...       │ │
│ │ (200자 요약)                                        │ │
│ │                                                     │ │
│ │ [카드뉴스 생성] [원본 보기] [북마크]                │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🔒 Security Update: October 2025                [>] │ │
│ │                                                     │ │
│ │ 📍 Microsoft Security Blog                          │ │
│ │ 🏷️  #Security #Update #Patch                       │ │
│ │ 📅 2025-10-28 14:00                                 │ │
│ │                                                     │ │
│ │ Critical security updates for Windows...           │ │
│ │ (200자 요약)                                        │ │
│ │                                                     │ │
│ │ [카드뉴스 생성] [원본 보기] [북마크]                │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 📢 Microsoft News: Cloud Expansion             [>] │ │
│ │ ...                                                 │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ [더 보기] (무한 스크롤 또는 페이지네이션)               │
└─────────────────────────────────────────────────────────┘
```

---

### 3. 카드 디자인 상세

#### 카드 구성 요소

```
┌─────────────────────────────────────────────────────────┐
│ [아이콘] [제목]                                   [액션]│
│ ┌─────────────────────────────────────────────────────┐ │
│ │                                                     │ │
│ │ 📰 제목 (60자 제한)                                 │ │
│ │    - 긴 제목은 말줄임표(...)로 처리                │ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ 📍 소스 출처: [사이트 이름]                             │
│ 🏷️  키워드: #키워드1 #키워드2 #키워드3 (최대 5개)      │
│ 📅 날짜: 2025-10-28 15:30 (또는 "3시간 전")            │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 요약 (200자 제한)                                   │ │
│ │                                                     │ │
│ │ AI가 생성한 게시물 요약 내용이 여기에 표시됩니다.  │ │
│ │ 사용자는 빠르게 내용을 파악할 수 있습니다...        │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ [🎨 카드뉴스 생성] [🔗 원본 보기] [⭐ 북마크]          │
└─────────────────────────────────────────────────────────┘
```

#### 카드 상태 표시

| 상태 | 표시 | 설명 |
|------|------|------|
| 신규 | 🆕 NEW | 최근 24시간 이내 |
| 읽음 | (없음) | 사용자가 이미 본 게시물 |
| 카드뉴스 생성됨 | ✅ 생성 완료 | 이미 카드뉴스가 생성된 게시물 |
| 생성 중 | ⏳ 생성 중 | 카드뉴스 생성 진행 중 |

---

### 4. 기능 상세

#### 4-1. 데이터 소스

RSS Library는 두 가지 소스에서 데이터를 가져옵니다:

1. **Firestore `projects` 컬렉션**
   - 이미 카드뉴스가 생성된 게시물
   - `source_type: 'rss'`
   - `source_site_id`, `original_published_at` 포함

2. **실시간 RSS 피드 (캐시)**
   - 등록된 RSS 사이트의 최신 피드
   - 카드뉴스가 아직 생성되지 않은 게시물
   - 메모리 캐시 (1시간 유효)

#### 4-2. 통합 및 정렬

```python
# 의사 코드
def get_rss_library_feed(filters):
    # 1. Firestore에서 RSS 프로젝트 가져오기
    projects = get_projects(source_type='rss')
    
    # 2. 실시간 RSS 피드에서 새 게시물 가져오기
    all_sites = get_all_sites(status='active')
    rss_posts = []
    for site in all_sites:
        posts = parse_rss_feed(site.rss_url)
        rss_posts.extend(posts)
    
    # 3. 통합 (중복 제거)
    combined = merge_and_deduplicate(projects, rss_posts)
    
    # 4. 시간순 정렬 (최신 → 과거)
    sorted_feed = sort_by_published_date(combined, descending=True)
    
    # 5. 필터링 (사이트, 날짜, 키워드)
    filtered = apply_filters(sorted_feed, filters)
    
    # 6. 페이지네이션
    return paginate(filtered, page_size=20)
```

#### 4-3. API 엔드포인트

**신규 API**

```python
GET /api/library/feed
Query Parameters:
  - site_id: string (optional) - 특정 사이트만 조회
  - start_date: date (optional) - 시작 날짜
  - end_date: date (optional) - 종료 날짜
  - keyword: string (optional) - 키워드 검색
  - page: int (default: 1) - 페이지 번호
  - page_size: int (default: 20) - 페이지 크기

Response:
{
  "total": 150,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "uuid",
      "type": "project" | "rss_post",  // 구분
      "title": "제목",
      "source": {
        "site_id": "uuid",
        "site_name": "Microsoft Blogs",
        "site_url": "https://blogs.microsoft.com"
      },
      "keywords": ["AI", "Innovation"],
      "summary": "요약 내용 (200자)",
      "published_at": "2025-10-28T15:30:00Z",
      "url": "https://...",
      "has_cardnews": true,  // 카드뉴스 생성 여부
      "project_id": "uuid" | null,  // 카드뉴스 프로젝트 ID
      "is_new": true  // 24시간 이내 여부
    }
  ]
}
```

**기존 API 확장**

```python
POST /api/library/create-cardnews
Request:
{
  "rss_post_id": "uuid",  // RSS 게시물 ID (URL을 해시한 값)
  "site_id": "uuid",
  "url": "https://...",
  "title": "제목",
  "content": "전체 내용"
}

Response:
{
  "project_id": "uuid",
  "status": "draft" | "summarized" | "completed"
}
```

---

### 5. Backend 개발

#### 5-1. 새 서비스 구현

**`backend/app/services/library_service.py`**

```python
"""RSS Library 서비스 - 통합 피드 제공"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import hashlib

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
        
        Returns:
            {
                'total': int,
                'page': int,
                'page_size': int,
                'items': List[FeedItem]
            }
        """
        # 1. Firestore에서 RSS 프로젝트 가져오기
        projects = self._get_projects_feed(site_id, start_date, end_date)
        
        # 2. 실시간 RSS 피드 가져오기 (캐시 활용)
        rss_posts = await self._get_rss_posts_feed(site_id)
        
        # 3. 통합 및 중복 제거
        combined = self._merge_feeds(projects, rss_posts)
        
        # 4. 필터링
        filtered = self._apply_filters(combined, keyword)
        
        # 5. 정렬 (최신순)
        sorted_feed = sorted(
            filtered,
            key=lambda x: x['published_at'],
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
    
    def _get_projects_feed(
        self,
        site_id: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Dict]:
        """Firestore에서 RSS 프로젝트 조회"""
        # Firestore 쿼리
        projects = get_all_projects(
            source_type='rss',
            site_id=site_id
        )
        
        # FeedItem 형식으로 변환
        feed_items = []
        for project in projects:
            feed_items.append({
                'id': project['id'],
                'type': 'project',
                'title': project.get('title', 'Untitled'),
                'source': {
                    'site_id': project.get('source_site_id'),
                    'site_name': project.get('source_site_name'),
                    'site_url': project.get('source_url')
                },
                'keywords': project.get('keywords', []),
                'summary': project.get('summary', ''),
                'published_at': project.get('original_published_at') or project.get('created_at'),
                'url': project.get('source_url'),
                'has_cardnews': True,
                'project_id': project['id'],
                'is_new': self._is_new(project.get('created_at'))
            })
        
        return feed_items
    
    async def _get_rss_posts_feed(
        self,
        site_id: Optional[str]
    ) -> List[Dict]:
        """실시간 RSS 피드에서 게시물 조회 (캐시 활용)"""
        # 캐시 확인
        cache_key = f"rss_feed_{site_id or 'all'}"
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if (datetime.now() - cached_time).total_seconds() < self.cache_ttl:
                return cached_data
        
        # RSS 피드 파싱
        sites = get_all_sites(status='active')
        if site_id:
            sites = [s for s in sites if s['id'] == site_id]
        
        feed_items = []
        for site in sites:
            posts = self.rss_service.parse_rss_feed(site['rss_url'])
            
            for post in posts:
                # 이미 프로젝트가 있는지 확인
                post_id = self._generate_post_id(post['link'])
                existing_project = self._check_existing_project(post_id)
                
                if not existing_project:
                    # 간단한 AI 요약 생성 (선택)
                    summary = await self._generate_quick_summary(post['content'])
                    keywords = await self._extract_quick_keywords(post['content'])
                    
                    feed_items.append({
                        'id': post_id,
                        'type': 'rss_post',
                        'title': post['title'],
                        'source': {
                            'site_id': site['id'],
                            'site_name': site['name'],
                            'site_url': site['url']
                        },
                        'keywords': keywords,
                        'summary': summary or post.get('summary', '')[:200],
                        'published_at': post['published'],
                        'url': post['link'],
                        'has_cardnews': False,
                        'project_id': None,
                        'is_new': self._is_new(post['published'])
                    })
        
        # 캐시 저장
        self.cache[cache_key] = (feed_items, datetime.now())
        
        return feed_items
    
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
            if url not in seen_urls:
                merged.append(item)
                seen_urls.add(url)
        
        # RSS 게시물 추가 (프로젝트에 없는 것만)
        for item in rss_posts:
            url = item['url']
            if url not in seen_urls:
                merged.append(item)
                seen_urls.add(url)
        
        return merged
    
    def _apply_filters(
        self,
        items: List[Dict],
        keyword: Optional[str]
    ) -> List[Dict]:
        """키워드 필터 적용"""
        if not keyword:
            return items
        
        keyword_lower = keyword.lower()
        filtered = []
        
        for item in items:
            # 제목, 요약, 키워드에서 검색
            if (keyword_lower in item['title'].lower() or
                keyword_lower in item['summary'].lower() or
                any(keyword_lower in k.lower() for k in item['keywords'])):
                filtered.append(item)
        
        return filtered
    
    def _is_new(self, published_at: datetime) -> bool:
        """24시간 이내 게시물인지 확인"""
        if not published_at:
            return False
        return (datetime.now() - published_at).total_seconds() < 86400
    
    def _generate_post_id(self, url: str) -> str:
        """URL을 해시하여 게시물 ID 생성"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _check_existing_project(self, post_id: str) -> Optional[Dict]:
        """URL 해시로 기존 프로젝트 확인"""
        # Firestore 쿼리 (URL 기반)
        pass
    
    async def _generate_quick_summary(self, content: str) -> str:
        """간단한 AI 요약 생성 (선택적)"""
        # OpenAI API 호출 (짧은 요약, 저렴한 모델)
        pass
    
    async def _extract_quick_keywords(self, content: str) -> List[str]:
        """간단한 키워드 추출 (선택적)"""
        # OpenAI API 호출 또는 간단한 알고리즘
        pass
```

#### 5-2. 새 라우터 추가

**`backend/app/routers/library.py`**

```python
"""RSS Library API"""

from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/library", tags=["library"])

@router.get("/feed")
async def get_library_feed(
    site_id: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    keyword: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    RSS Library 통합 피드 조회
    
    - 등록된 모든 RSS 사이트의 게시물을 시간순으로 조회
    - 카드뉴스가 생성된 게시물과 미생성 게시물 모두 포함
    """
    library_service = LibraryService()
    
    result = await library_service.get_feed(
        site_id=site_id,
        start_date=start_date,
        end_date=end_date,
        keyword=keyword,
        page=page,
        page_size=page_size
    )
    
    return result

@router.post("/create-cardnews")
async def create_cardnews_from_feed(
    rss_post_id: str,
    site_id: str,
    url: str,
    title: str,
    content: str
):
    """
    RSS Library에서 카드뉴스 생성
    
    - RSS 게시물을 카드뉴스 프로젝트로 변환
    """
    # 자동 생성 파이프라인 실행
    pipeline = AutoGenerationPipeline(model='gpt-4.1-nano')
    
    post = {
        'id': rss_post_id,
        'title': title,
        'link': url,
        'content': content,
        'published': datetime.now()
    }
    
    site = get_site(site_id)
    
    project_id = await pipeline.generate_cardnews_from_post(
        post=post,
        site_id=site_id,
        site_name=site['name']
    )
    
    return {
        'project_id': project_id,
        'status': 'success'
    }
```

---

### 6. Frontend 개발

#### 6-1. 새 페이지 추가

**`frontend/app/library/page.tsx`**

```typescript
'use client';

import { useState, useEffect } from 'react';
import { LibraryFeedItem } from '@/types/library';
import { FeedCard } from '@/components/library/FeedCard';
import { FeedFilters } from '@/components/library/FeedFilters';

export default function LibraryPage() {
  const [feed, setFeed] = useState<LibraryFeedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    siteId: null,
    keyword: '',
    page: 1
  });

  useEffect(() => {
    loadFeed();
  }, [filters]);

  const loadFeed = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `/api/library/feed?` + new URLSearchParams({
          ...(filters.siteId && { site_id: filters.siteId }),
          ...(filters.keyword && { keyword: filters.keyword }),
          page: filters.page.toString()
        })
      );
      const data = await response.json();
      setFeed(data.items);
    } catch (error) {
      console.error('Failed to load feed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">RSS Library</h1>
      
      <FeedFilters 
        filters={filters}
        onChange={setFilters}
      />
      
      <div className="space-y-4 mt-8">
        {loading ? (
          <div>Loading...</div>
        ) : (
          feed.map(item => (
            <FeedCard key={item.id} item={item} />
          ))
        )}
      </div>
    </div>
  );
}
```

#### 6-2. 피드 카드 컴포넌트

**`frontend/components/library/FeedCard.tsx`**

```typescript
'use client';

import { LibraryFeedItem } from '@/types/library';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

interface FeedCardProps {
  item: LibraryFeedItem;
}

export function FeedCard({ item }: FeedCardProps) {
  const handleCreateCardnews = async () => {
    // 카드뉴스 생성 로직
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      {/* 헤더 */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            {item.is_new && (
              <span className="inline-block px-2 py-1 text-xs font-bold text-white bg-red-500 rounded mr-2">
                NEW
              </span>
            )}
            {item.title}
          </h3>
        </div>
        
        {item.has_cardnews && (
          <span className="inline-block px-3 py-1 text-sm font-semibold text-green-600 bg-green-100 rounded">
            ✅ 생성 완료
          </span>
        )}
      </div>

      {/* 메타 정보 */}
      <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
        <div className="flex items-center gap-1">
          <span>📍</span>
          <span>{item.source.site_name}</span>
        </div>
        
        <div className="flex items-center gap-1">
          <span>📅</span>
          <span>{formatDistanceToNow(new Date(item.published_at), { addSuffix: true, locale: ko })}</span>
        </div>
      </div>

      {/* 키워드 */}
      {item.keywords.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {item.keywords.slice(0, 5).map(keyword => (
            <span
              key={keyword}
              className="inline-block px-3 py-1 text-sm font-medium text-blue-600 bg-blue-50 rounded-full"
            >
              #{keyword}
            </span>
          ))}
        </div>
      )}

      {/* 요약 */}
      <p className="text-gray-700 mb-6 line-clamp-3">
        {item.summary}
      </p>

      {/* 액션 버튼 */}
      <div className="flex gap-3">
        {!item.has_cardnews ? (
          <button
            onClick={handleCreateCardnews}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            🎨 카드뉴스 생성
          </button>
        ) : (
          <a
            href={`/edit/${item.project_id}`}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            ✏️ 편집하기
          </a>
        )}
        
        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
        >
          🔗 원본 보기
        </a>
      </div>
    </div>
  );
}
```

---

## 🔧 성능 최적화

### 1. Firestore 복합 인덱스 생성

**필요한 인덱스**
```javascript
// firestore.indexes.json
{
  "indexes": [
    {
      "collectionGroup": "crawl_logs",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "site_id", "order": "ASCENDING" },
        { "fieldPath": "started_at", "order": "DESCENDING" }
      ]
    },
    {
      "collectionGroup": "projects",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "source_type", "order": "ASCENDING" },
        { "fieldPath": "original_published_at", "order": "DESCENDING" }
      ]
    },
    {
      "collectionGroup": "projects",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "source_site_id", "order": "ASCENDING" },
        { "fieldPath": "original_published_at", "order": "DESCENDING" }
      ]
    }
  ]
}
```

### 2. MetaMask 코드 제거

**제거할 파일/코드**
- 검색: "MetaMask", "metamask", "ethereum", "web3"
- 관련 코드 모두 제거
- 불필요한 의존성 제거

### 3. 캐싱 전략

**Redis 캐시 도입 (선택)**
- RSS 피드 캐시 (1시간)
- Library 피드 캐시 (10분)
- 사이트 목록 캐시 (30분)

---

## 📊 예상 일정

### Day 1-2: RSS Library Backend
- [x] `library_service.py` 구현
- [x] `library.py` 라우터 추가
- [x] API 테스트

### Day 3-4: RSS Library Frontend
- [x] `/library` 페이지 구현
- [x] FeedCard 컴포넌트
- [x] FeedFilters 컴포넌트
- [x] 카드뉴스 생성 연동

### Day 5: 성능 최적화
- [x] Firestore 인덱스 생성
- [x] MetaMask 코드 제거
- [x] 캐싱 구현

### Day 6: 테스트 및 버그 수정
- [x] End-to-end 테스트
- [x] 성능 테스트
- [x] 버그 수정

### Day 7: 배포 및 문서화
- [x] 프로덕션 배포
- [x] 문서 업데이트
- [x] 완료 보고서 작성

---

## 🎯 성공 지표

### 기능
- [x] RSS Library 페이지 접근 가능
- [x] 모든 RSS 게시물이 시간순으로 표시
- [x] 필터링 (사이트, 키워드) 정상 작동
- [x] 카드뉴스 생성 버튼 작동
- [x] 원본 보기 링크 작동

### 성능
- [x] Library 피드 로딩 시간 < 2초
- [x] 페이지네이션 (20개 단위)
- [x] 무한 스크롤 또는 "더 보기" 버튼

### UX
- [x] 카드 디자인 일관성
- [x] 반응형 디자인 (모바일 지원)
- [x] 로딩 상태 표시
- [x] 에러 처리

---

## 📝 참고 사항

### 기술적 고려사항
1. **중복 제거**: URL 기반 중복 제거 (MD5 해시)
2. **캐싱**: 메모리 캐시 (1시간 TTL)
3. **페이지네이션**: 20개 단위
4. **AI 요약**: 선택적 (비용 고려)

### 제약사항
1. **Firestore 쿼리**: 복합 인덱스 필요
2. **RSS 파싱**: 느린 사이트는 타임아웃
3. **메모리**: 캐시 크기 제한

### 향후 개선
1. **북마크 기능**: 사용자가 관심 게시물 저장
2. **읽음 표시**: 사용자가 본 게시물 추적
3. **알림**: 새 게시물 알림
4. **추천 시스템**: AI 기반 게시물 추천

---

---

## ✅ Phase 2.5 완료 현황

### 📊 개발 통계
- **전체 진행률**: 100% ✅
- **개발 기간**: 1일 (2025-10-28)
- **신규 API**: 2개 엔드포인트
- **신규 페이지**: 2개 (Library, Generating)
- **신규 컬렉션**: 1개 (rss_posts)
- **처리된 RSS 게시물**: 100+ (자동 번역 및 요약)

### 🎯 주요 성과
1. ✅ **RSS Library 구축 완료**
   - 모든 RSS 게시물 통합 조회
   - 월별/사이트별 필터링
   - 키워드 검색
   - 카드 형태 UI

2. ✅ **자동 AI 처리 파이프라인 구축**
   - RSS 크롤링 시 자동 요약 (8-12문장, 한글)
   - 자동 키워드 추출 (최대 5개, 한글)
   - 제목 한글 번역 (영문 → 한글)
   - 기존 게시물 마이그레이션 완료

3. ✅ **UX 대폭 개선**
   - 카드뉴스 생성 로딩 페이지 (스피닝 + 진행 단계)
   - Undo 기능 (AI 수정 복원)
   - 목록 버튼 동적 이동 (RSS → Library, 일반 → Projects)
   - 키워드 태그 표시
   - 실제 날짜/시간 표시

4. ✅ **한글 생성 강화**
   - 모든 카드뉴스 한글 생성
   - 영문 원본도 자동 번역
   - 프롬프트 및 시스템 메시지 강화

### 🚀 완료된 기능 목록

#### Backend
- ✅ `rss_posts` 컬렉션 추가
- ✅ `GET /api/library/feed` API
- ✅ `POST /api/library/create-cardnews` API
- ✅ RSS 크롤러 자동 AI 처리
- ✅ `migrate_rss_posts.py` 마이그레이션 스크립트
- ✅ 한글 생성 프롬프트 강화
- ✅ 에러 처리 개선

#### Frontend
- ✅ `/library` 페이지 (RSS Library)
- ✅ `/generating` 페이지 (로딩 페이지)
- ✅ `FeedCard` 컴포넌트 (키워드, 날짜, 상태)
- ✅ `FeedFilters` 컴포넌트 (월별, 사이트별 필터)
- ✅ Undo 기능 (ChatInterface, EditPage)
- ✅ 목록 버튼 동적 이동
- ✅ `date-fns` 라이브러리 추가

### 📝 주요 변경사항

#### 데이터 모델
```python
# RSSPost (새 컬렉션)
- title: str (한글 제목)
- title_original: Optional[str] (원문 제목)
- summary: str (AI 요약, 한글)
- keywords: List[str] (AI 추출 키워드)
- has_cardnews: bool (카드뉴스 생성 여부)
- project_id: Optional[str] (연결된 프로젝트 ID)
```

#### AI 프롬프트
```python
# 카드 생성 프롬프트 강화
"🚨 최우선 지시사항: 모든 카드 내용을 반드시 한글로 작성하세요! 🚨"
"Even if the original text is in English, translate and write in Korean!"

# 시스템 메시지
"You are a Korean card news creation expert. 
You MUST write ALL content in KOREAN (한글) only!"
```

### 🐛 해결된 주요 이슈
1. ✅ 영문 원본이 영어로 생성되는 문제 → 한글 우선 프롬프트
2. ✅ `recommended_card_count` None 에러 → `or 5` 처리
3. ✅ 짧은 콘텐츠 500 에러 → 명확한 400 에러 메시지
4. ✅ 요약 페이지 422 에러 → Request Body 방식 변경
5. ✅ 영문 스크래핑 실패 → 3단계 언어 감지 폴백
6. ✅ Library 무한 로딩 → APScheduler 주석 처리
7. ✅ MetaMask 에러 → 완전 제거

---

## 🔗 관련 문서

- **Phase 2 완료 보고서**: `docs/PHASE2_COMPLETE.md`
- **Phase 2 개발 정의서**: `PHASE2_SPEC.md`
- **Phase 2.5 완료 보고서**: `docs/PHASE2_5_COMPLETE.md` 🆕
- **TODO**: `TODO.md`
- **PRD**: `docs/PRD.md`
- **개발 문서**: `docs/개발문서.md`

---

**문서 작성일**: 2025-10-28  
**최종 업데이트**: 2025-10-28  
**작성자**: AI Development Team  
**버전**: 1.1.0  
**상태**: ✅ Phase 2.5 완료

