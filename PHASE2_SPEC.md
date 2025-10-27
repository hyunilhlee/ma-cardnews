# Phase 2 개발 정의서 - RSS 기반 자동화 시스템

**CardNews AI Generator - RSS Auto-Generation Phase**

**작성일**: 2025-10-26 (업데이트)  
**예상 개발 기간**: 3-4주 ⚡ (1-2주 단축!)  
**개발 우선순위**: High

---

## 📋 목차

1. [개요](#1-개요)
2. [핵심 목표](#2-핵심-목표)
3. [시스템 아키텍처](#3-시스템-아키텍처)
4. [데이터베이스 설계](#4-데이터베이스-설계)
5. [기능 상세 명세](#5-기능-상세-명세)
6. [API 명세](#6-api-명세)
7. [크롤링 전략](#7-크롤링-전략)
8. [자동화 파이프라인](#8-자동화-파이프라인)
9. [UI/UX 설계](#9-uiux-설계)
10. [기술 스택](#10-기술-스택)
11. [개발 일정](#11-개발-일정)
12. [테스트 계획](#12-테스트-계획)

---

## 1. 개요

### 1.1 Phase 2의 목적

Phase 1에서는 사용자가 **직접 URL이나 텍스트를 입력**하여 카드뉴스를 생성했습니다.

Phase 2에서는 시스템이 **등록된 사이트를 자동으로 모니터링**하여, 새 게시물이 올라오면 **사용자 개입 없이 카드뉴스를 생성**하고 **이메일로 알림**을 보냅니다.

### 1.2 핵심 가치

| 항목 | Phase 1 (수동) | Phase 2 (RSS 자동) |
|------|---------------|-------------------|
| **콘텐츠 발견** | 사용자가 직접 찾아서 입력 | RSS 피드로 자동 감지 |
| **크롤링 방식** | 수동 URL 입력 | RSS 파싱 (간단하고 빠름) |
| **생성 방식** | 사용자가 "생성" 버튼 클릭 | 완전 자동 생성 |
| **알림** | 없음 | 사용자 등록 이메일로 발송 |
| **저장** | 인메모리 (휘발성) | DB 영구 저장 |
| **수정** | 즉시 수정 | 나중에 검토 후 수정 |
| **개발 복잡도** | - | **낮음** (RSS만 지원) ⚡ |

### 1.3 사용 시나리오

**시나리오**: Microsoft 보안 블로그 모니터링

1. 사용자가 https://www.microsoft.com/en-us/security 를 크롤링 사이트로 등록
2. 시스템이 15분마다 자동으로 RSS 피드를 체크
3. 새 게시물 발견: "New Zero-Day Vulnerability Discovered"
4. 시스템이 자동으로:
   - 게시물 스크래핑
   - AI 요약 생성
   - 카드뉴스 5장 자동 생성
   - DB에 "초안" 상태로 저장
   - 사용자에게 이메일 발송: "새 카드뉴스가 생성되었습니다!"
5. 사용자가 이메일 링크를 클릭하여 프로젝트 확인
6. 필요시 요약 또는 카드 내용을 수정
7. "완료" 버튼 클릭하여 최종 확정

---

## 2. 핵심 목표

### 2.1 기능적 목표

- ✅ **RSS 자동 크롤링**: RSS 피드에서 새 게시물 자동 감지 (간단하고 빠름)
- ✅ **100% 자동 생성**: 사용자 개입 없이 카드뉴스 완성
- ✅ **영구 저장**: Firebase Firestore에 모든 프로젝트 저장
- ✅ **사용자별 이메일 알림**: 대시보드에서 이메일 등록/관리
- ✅ **프로젝트 관리**: 저장/수정/삭제/버전 관리
- ⚡ **빠른 개발**: 복잡한 웹 스크래핑 제외, RSS만 지원

### 2.2 비기능적 목표

- ⚡ **성능**: 크롤링 1회당 10초 이내
- 🔒 **안정성**: 크롤링 실패 시 3회 자동 재시도
- 📈 **확장성**: 최대 100개 사이트 동시 모니터링 지원
- 🛡️ **보안**: 크롤링 Rate Limit 준수 (1분당 최대 10회)

### 2.3 성공 지표

| 지표 | 목표 |
|------|------|
| 크롤링 성공률 | 95% 이상 |
| 카드뉴스 생성 성공률 | 90% 이상 |
| 이메일 발송 성공률 | 99% 이상 |
| 평균 응답 시간 | 30초 이내 |

---

## 3. 시스템 아키텍처

### 3.1 전체 구조

```
┌─────────────────────────────────────────────────────────────┐
│                         사용자                               │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ 크롤링 설정  │ │ Phase 1 생성 │ │프로젝트 관리 │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└───────────────────┬─────────────────────────────────────────┘
                    │ REST API
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                 Backend (FastAPI)                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │            Scheduler (APScheduler)                     │  │
│  │    - 크롤링 작업 스케줄링 (5분/15분/30분/1시간)       │  │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │                                   │
│  ┌───────────────────────▼───────────────────────────────┐  │
│  │           Crawler Service                              │  │
│  │  ┌──────────────┐  ┌──────────────┐                  │  │
│  │  │ RSS Parser   │  │ Web Scraper  │                  │  │
│  │  │ (feedparser) │  │ (Playwright) │                  │  │
│  │  └──────────────┘  └──────────────┘                  │  │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │                                   │
│  ┌───────────────────────▼───────────────────────────────┐  │
│  │        Auto-Generation Pipeline                        │  │
│  │  1. 스크래핑 → 2. 요약 → 3. 생성 → 4. 저장 → 5. 알림 │  │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │                                   │
│  ┌───────────────────────▼───────────────────────────────┐  │
│  │           Email Service (SendGrid)                     │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                Firebase Firestore (Database)                 │
│  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌──────────┐     │
│  │  sites   │ │ projects │ │crawl_logs │ │notifications│    │
│  └──────────┘ └──────────┘ └───────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 데이터 흐름

```
[새 게시물 발행]
       ↓
[Scheduler가 크롤링 트리거]
       ↓
[RSS Parser 또는 Web Scraper 실행]
       ↓
[새 게시물 감지 및 본문 추출]
       ↓
[Auto-Generation Pipeline 시작]
       ↓
┌─────────────────────────────┐
│ 1. Scraper Service          │ → 본문 추출
│ 2. Summarizer Service       │ → AI 요약
│ 3. Card Generator Service   │ → 카드 생성
│ 4. Firestore 저장           │ → "초안" 상태
│ 5. Email Service            │ → 알림 발송
└─────────────────────────────┘
       ↓
[사용자 이메일 수신]
       ↓
[프로젝트 확인 및 수정]
       ↓
[최종 저장 ("완료" 상태)]
```

---

## 4. 데이터베이스 설계

### 4.1 Firestore 컬렉션 구조

#### **Collection: `sites`**
등록된 크롤링 사이트 정보

```javascript
{
  "id": "site_001",
  "name": "Microsoft Security Blog",
  "url": "https://www.microsoft.com/en-us/security",
  "rss_url": "https://www.microsoft.com/en-us/security/rss", // 선택사항
  "crawl_type": "rss" | "web", // RSS 또는 웹 스크래핑
  "crawl_interval": 15, // 분 단위 (5, 15, 30, 60)
  "is_active": true,
  "last_crawled_at": "2025-10-25T10:30:00Z",
  "last_post_id": "post_12345", // 중복 방지용
  "created_at": "2025-10-20T09:00:00Z",
  "updated_at": "2025-10-25T10:30:00Z",
  "crawl_stats": {
    "total_crawls": 150,
    "successful_crawls": 145,
    "failed_crawls": 5,
    "total_posts_found": 23
  }
}
```

#### **Collection: `projects`**
생성된 카드뉴스 프로젝트

```javascript
{
  "id": "proj_001",
  "title": "New Zero-Day Vulnerability Discovered",
  "source_type": "auto" | "manual", // 자동 생성 vs 수동 생성
  "source_site_id": "site_001", // sites 컬렉션 참조
  "source_url": "https://www.microsoft.com/en-us/security/blog/...",
  "original_text": "Full article text...",
  "summary": "AI-generated summary...",
  "keywords": ["security", "zero-day", "vulnerability"],
  "card_count": 5,
  "status": "draft" | "review" | "completed" | "archived",
  "ai_model": "gpt-4.1-nano",
  "language": "en" | "ko" | "ja",
  "version": 1, // 버전 관리
  "sections": [
    {
      "id": "sec_001",
      "type": "title",
      "title": "Breaking Security News",
      "content": "Microsoft discovers new vulnerability",
      "order": 0
    },
    // ... more sections
  ],
  "created_at": "2025-10-25T10:35:00Z",
  "updated_at": "2025-10-25T11:00:00Z",
  "notification_sent": true,
  "notification_sent_at": "2025-10-25T10:36:00Z",
  "metadata": {
    "generation_time_ms": 12500,
    "auto_generated": true,
    "user_modified": false
  }
}
```

#### **Collection: `crawl_logs`**
크롤링 실행 이력

```javascript
{
  "id": "log_001",
  "site_id": "site_001",
  "crawl_type": "rss" | "web",
  "status": "success" | "failed" | "partial",
  "started_at": "2025-10-25T10:30:00Z",
  "completed_at": "2025-10-25T10:30:08Z",
  "duration_ms": 8000,
  "posts_found": 2,
  "posts_new": 1,
  "posts_skipped": 1, // 중복
  "error_message": null, // 실패 시 에러 메시지
  "retry_count": 0
}
```

#### **Collection: `notifications`**
이메일 알림 이력

```javascript
{
  "id": "notif_001",
  "project_id": "proj_001",
  "notification_type": "card_generated" | "crawl_failed" | "weekly_summary",
  "recipient_email": "user@example.com",
  "subject": "New Card News Generated",
  "sent_at": "2025-10-25T10:36:00Z",
  "status": "sent" | "failed",
  "sendgrid_message_id": "msg_12345"
}
```

### 4.2 인덱스 설계

**필수 인덱스**:
- `projects`: `status`, `created_at` (desc)
- `projects`: `source_site_id`, `created_at` (desc)
- `crawl_logs`: `site_id`, `started_at` (desc)
- `sites`: `is_active`, `last_crawled_at` (asc)

---

## 5. 기능 상세 명세

### 5.1 크롤링 사이트 관리

#### **Feature 5.1.1: 사이트 등록**

**화면**: 크롤링 사이트 설정 페이지 → "새 사이트 추가" 버튼

**입력 필드**:
- 사이트 이름 (필수)
- 사이트 URL (필수)
- RSS URL (선택)
- 크롤링 방식: RSS / 웹 스크래핑 (자동 감지 우선)
- 크롤링 주기: 5분 / 15분 / 30분 / 1시간
- 활성화 여부: ON / OFF

**유효성 검사**:
- URL 형식 검증
- 중복 URL 체크
- RSS 피드 유효성 확인 (RSS 선택 시)

**처리 로직**:
1. URL 유효성 검사
2. RSS 자동 감지 시도
3. Firestore `sites` 컬렉션에 저장
4. 즉시 첫 크롤링 실행 (테스트)
5. 스케줄러에 작업 등록

#### **Feature 5.1.2: 사이트 목록 조회**

**화면**: 크롤링 사이트 설정 페이지

**표시 정보**:
- 사이트 이름, URL
- 활성화 상태 (토글)
- 마지막 크롤링 시간
- 다음 예정 시간
- 크롤링 통계 (성공/실패 횟수, 발견된 게시물 수)
- 수동 크롤링 버튼

**필터/정렬**:
- 활성/비활성
- 최근 크롤링 순

#### **Feature 5.1.3: Microsoft 기본 사이트**

**자동 등록**:
앱 최초 실행 시 3개 사이트 자동 등록 (비활성 상태)

1. **Microsoft Blogs**
   - URL: https://blogs.microsoft.com/
   - RSS: https://blogs.microsoft.com/feed/
   - 주기: 30분

2. **Microsoft News Korea**
   - URL: https://news.microsoft.com/source/asia/region/korea/?lang=ko
   - RSS: 자동 감지
   - 주기: 15분

3. **Microsoft Security**
   - URL: https://www.microsoft.com/en-us/security
   - RSS: https://www.microsoft.com/en-us/security/rss
   - 주기: 15분

### 5.2 자동 크롤링 시스템

#### **Feature 5.2.1: RSS 피드 파싱**

**라이브러리**: `feedparser`

**처리 흐름**:
```python
import feedparser

def parse_rss_feed(rss_url, last_post_id):
    feed = feedparser.parse(rss_url)
    new_posts = []
    
    for entry in feed.entries:
        post_id = entry.id or entry.link
        
        # 중복 체크
        if post_id == last_post_id:
            break
        
        new_posts.append({
            'id': post_id,
            'title': entry.title,
            'url': entry.link,
            'published_at': entry.published_parsed,
            'summary': entry.summary if hasattr(entry, 'summary') else ''
        })
    
    return new_posts
```

**에러 처리**:
- RSS 파싱 실패 → 웹 스크래핑으로 Fallback
- 네트워크 타임아웃 → 3회 재시도
- 빈 피드 → 로그 기록, 다음 주기 대기

#### **Feature 5.2.2: 웹 스크래핑 (Playwright)**

**라이브러리**: `playwright`

**처리 흐름**:
```python
from playwright.async_api import async_playwright

async def scrape_website(url, last_post_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state('networkidle')
        
        # 사이트별 커스텀 셀렉터
        posts = await page.query_selector_all('.post-item')
        
        new_posts = []
        for post in posts:
            post_url = await post.get_attribute('href')
            if post_url == last_post_id:
                break
            
            title = await post.query_selector('.title')
            # ... 추출 로직
            
        await browser.close()
        return new_posts
```

**사이트별 커스텀 설정**:
```python
SITE_SELECTORS = {
    'blogs.microsoft.com': {
        'post_list': '.entry-box',
        'post_link': 'a.entry-title-link',
        'post_title': '.entry-title'
    },
    # ... 다른 사이트
}
```

#### **Feature 5.2.3: 스케줄러**

**라이브러리**: `APScheduler`

**스케줄러 설정**:
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# 사이트별 동적 작업 등록
def register_site_job(site):
    scheduler.add_job(
        func=crawl_site,
        trigger='interval',
        minutes=site.crawl_interval,
        args=[site.id],
        id=f'crawl_{site.id}',
        replace_existing=True
    )

# 앱 시작 시 모든 활성 사이트 등록
async def init_scheduler():
    sites = await get_active_sites()
    for site in sites:
        register_site_job(site)
    scheduler.start()
```

### 5.3 자동 생성 파이프라인

#### **Feature 5.3.1: 파이프라인 오케스트레이션**

**클래스 설계**:
```python
class AutoGenerationPipeline:
    def __init__(self, post_data, site_id):
        self.post_data = post_data
        self.site_id = site_id
        self.project_id = None
        
    async def run(self):
        try:
            # 1. 스크래핑
            text = await self.scrape_post()
            
            # 2. 요약
            summary_data = await self.summarize_text(text)
            
            # 3. 카드 생성
            sections = await self.generate_cards(text, summary_data)
            
            # 4. DB 저장
            self.project_id = await self.save_project(sections)
            
            # 5. 이메일 발송
            await self.send_notification()
            
            return self.project_id
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            await self.handle_failure(e)
            raise
```

**단계별 처리 시간 목표**:
| 단계 | 목표 시간 |
|------|----------|
| 스크래핑 | 5초 |
| 요약 | 8초 |
| 카드 생성 | 10초 |
| DB 저장 | 2초 |
| 이메일 | 3초 |
| **합계** | **28초** |

### 5.4 프로젝트 관리

#### **Feature 5.4.1: 프로젝트 목록**

**화면 레이아웃**:
```
┌─────────────────────────────────────────┐
│  저장된 프로젝트                         │
├─────────────────────────────────────────┤
│  [초안] [검토중] [완료]  [검색 🔍]      │
├─────────────────────────────────────────┤
│  ┌──────────────────┐ ┌──────────────┐ │
│  │ 📰 New Zero-Day  │ │ 📰 AI Update │ │
│  │ 🆕 2시간 전       │ │ 어제          │ │
│  │ Microsoft Security│ │ MS Blogs     │ │
│  │ [초안] [5 cards]  │ │ [완료] [6]   │ │
│  └──────────────────┘ └──────────────┘ │
└─────────────────────────────────────────┘
```

**필터링**:
- 상태별: 초안 / 검토중 / 완료 / 전체
- 날짜별: 오늘 / 이번 주 / 이번 달
- 소스별: 사이트 선택

**정렬**:
- 최신 순 (기본)
- 오래된 순
- 제목순 (A-Z)

#### **Feature 5.4.2: 프로젝트 상세 및 수정**

**상세 페이지 구성**:
```
┌─────────────────────────────────────────────┐
│ 📰 New Zero-Day Vulnerability Discovered    │
├─────────────────────────────────────────────┤
│ 소스: Microsoft Security                    │
│ 생성: 2025-10-25 10:35                      │
│ 상태: [초안 ▼]                              │
│                                             │
│ [요약 단계로 돌아가기] [카드 수정하기]      │
├─────────────────────────────────────────────┤
│  Card 1: [Breaking Security News]          │
│  Card 2: [What is Zero-Day?]               │
│  Card 3: [Impact Analysis]                 │
│  Card 4: [Mitigation Steps]                │
│  Card 5: [Learn More]                      │
├─────────────────────────────────────────────┤
│  [삭제] [복사] [완료 처리]                  │
└─────────────────────────────────────────────┘
```

**수정 모드 1: 요약 단계**
- 요약문 텍스트 수정
- 키워드 추가/삭제
- 카드 수 조절 (3-10장)
- "재생성" 버튼 → 새 버전 생성

**수정 모드 2: 카드 단계**
- Phase 1의 AI 채팅 UI 재사용
- 특정 카드 수정
- 전체 수정 (자연어)
- 실시간 프리뷰

### 5.5 이메일 알림

#### **Feature 5.5.1: SendGrid 통합**

**환경 변수**:
```env
SENDGRID_API_KEY=SG.xxx
ADMIN_EMAIL=admin@example.com
```

**이메일 템플릿 (HTML)**:

**템플릿 1: 카드뉴스 생성 완료**
```html
<!DOCTYPE html>
<html>
<body>
  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #0078d4;">📰 새 카드뉴스가 생성되었습니다!</h1>
    
    <div style="background: #f5f5f5; padding: 20px; border-radius: 8px;">
      <h2>{{ project_title }}</h2>
      <p><strong>출처:</strong> {{ source_name }}</p>
      <p><strong>생성 시간:</strong> {{ created_at }}</p>
      <p><strong>카드 수:</strong> {{ card_count }}장</p>
    </div>
    
    <p style="margin: 30px 0;">
      아래 버튼을 클릭하여 카드뉴스를 확인하고 수정하세요.
    </p>
    
    <a href="{{ project_url }}" 
       style="display: inline-block; background: #0078d4; color: white; 
              padding: 12px 24px; text-decoration: none; border-radius: 4px;">
      프로젝트 보기
    </a>
    
    <p style="margin-top: 30px; color: #666; font-size: 12px;">
      알림을 받고 싶지 않으신가요? 
      <a href="{{ settings_url }}">알림 설정</a>에서 변경하세요.
    </p>
  </div>
</body>
</html>
```

**전송 로직**:
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

async def send_card_generated_email(project):
    message = Mail(
        from_email='noreply@cardnews.ai',
        to_emails='user@example.com',
        subject=f'새 카드뉴스: {project.title}',
        html_content=render_template('card_generated.html', project=project)
    )
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        
        # 알림 이력 저장
        await save_notification_log(project.id, 'sent', response.message_id)
        
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        await save_notification_log(project.id, 'failed', str(e))
```

---

## 6. API 명세

### 6.1 크롤링 사이트 관리 API

#### `POST /api/sites`
사이트 등록

**Request**:
```json
{
  "name": "Microsoft Security Blog",
  "url": "https://www.microsoft.com/en-us/security",
  "rss_url": "https://www.microsoft.com/en-us/security/rss",
  "crawl_type": "rss",
  "crawl_interval": 15,
  "is_active": true
}
```

**Response** (201):
```json
{
  "id": "site_001",
  "name": "Microsoft Security Blog",
  "url": "https://www.microsoft.com/en-us/security",
  "is_active": true,
  "created_at": "2025-10-25T10:00:00Z"
}
```

#### `GET /api/sites`
사이트 목록 조회

**Query Parameters**:
- `is_active`: true/false (선택)
- `sort_by`: name/created_at/last_crawled_at
- `order`: asc/desc

**Response** (200):
```json
{
  "sites": [
    {
      "id": "site_001",
      "name": "Microsoft Security Blog",
      "url": "https://www.microsoft.com/en-us/security",
      "is_active": true,
      "last_crawled_at": "2025-10-25T10:30:00Z",
      "crawl_stats": {
        "total_crawls": 150,
        "successful_crawls": 145,
        "total_posts_found": 23
      }
    }
  ],
  "total": 1
}
```

#### `PUT /api/sites/{site_id}`
사이트 수정

#### `DELETE /api/sites/{site_id}`
사이트 삭제

#### `POST /api/sites/{site_id}/crawl`
수동 크롤링 트리거

**Response** (200):
```json
{
  "job_id": "job_12345",
  "status": "started",
  "estimated_time_sec": 10
}
```

### 6.2 프로젝트 관리 API

#### `GET /api/projects`
프로젝트 목록 조회

**Query Parameters**:
- `status`: draft/review/completed
- `source_site_id`: 사이트 ID
- `limit`: 10 (기본값)
- `offset`: 0

**Response** (200):
```json
{
  "projects": [
    {
      "id": "proj_001",
      "title": "New Zero-Day Vulnerability",
      "status": "draft",
      "source_site_id": "site_001",
      "card_count": 5,
      "created_at": "2025-10-25T10:35:00Z",
      "thumbnail_url": "https://..."
    }
  ],
  "total": 15,
  "limit": 10,
  "offset": 0
}
```

#### `GET /api/projects/{project_id}`
프로젝트 상세 조회

**Response** (200):
```json
{
  "id": "proj_001",
  "title": "New Zero-Day Vulnerability Discovered",
  "source_url": "https://...",
  "summary": "AI-generated summary...",
  "keywords": ["security", "zero-day"],
  "status": "draft",
  "version": 1,
  "sections": [...],
  "created_at": "2025-10-25T10:35:00Z"
}
```

#### `PUT /api/projects/{project_id}`
프로젝트 수정 (상태 변경, 내용 수정)

#### `DELETE /api/projects/{project_id}`
프로젝트 삭제 (소프트 삭제)

#### `POST /api/projects/{project_id}/regenerate`
요약 단계에서 재생성

**Request**:
```json
{
  "summary": "Updated summary...",
  "keywords": ["new", "keywords"],
  "card_count": 6
}
```

### 6.3 파이프라인 API

#### `POST /api/pipeline/trigger`
수동 파이프라인 트리거 (테스트용)

**Request**:
```json
{
  "post_url": "https://www.microsoft.com/en-us/security/blog/...",
  "site_id": "site_001"
}
```

**Response** (200):
```json
{
  "job_id": "pipeline_001",
  "status": "started",
  "estimated_time_sec": 30
}
```

#### `GET /api/pipeline/status/{job_id}`
파이프라인 상태 확인

**Response** (200):
```json
{
  "job_id": "pipeline_001",
  "status": "running" | "completed" | "failed",
  "current_step": "generating_cards",
  "progress_pct": 60,
  "project_id": "proj_001" // 완료 시
}
```

---

## 7. 크롤링 전략

### 7.1 Microsoft 사이트별 전략

#### **7.1.1 blogs.microsoft.com**

**RSS 피드**: ✅ 있음
- URL: https://blogs.microsoft.com/feed/
- 업데이트 빈도: 하루 2-3회
- 권장 주기: 30분

**파싱 로직**:
```python
def parse_microsoft_blogs():
    feed_url = 'https://blogs.microsoft.com/feed/'
    feed = feedparser.parse(feed_url)
    
    posts = []
    for entry in feed.entries[:5]:  # 최근 5개만
        posts.append({
            'title': entry.title,
            'url': entry.link,
            'published': entry.published,
            'author': entry.author if hasattr(entry, 'author') else '',
            'categories': [tag.term for tag in entry.tags]
        })
    
    return posts
```

#### **7.1.2 news.microsoft.com/korea**

**RSS 피드**: ⚠️ 확인 필요
- 한국어 사이트
- JavaScript 렌더링 가능성 → Playwright 사용

**Playwright 스크래핑**:
```python
async def scrape_microsoft_news_korea():
    url = 'https://news.microsoft.com/source/asia/region/korea/?lang=ko'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        
        # 게시물 목록 대기
        await page.wait_for_selector('.article-list-item')
        
        # 게시물 추출
        posts = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('.article-list-item')).map(item => ({
                title: item.querySelector('.article-title').innerText,
                url: item.querySelector('a').href,
                date: item.querySelector('.article-date').innerText
            }));
        }''')
        
        await browser.close()
        return posts
```

#### **7.1.3 microsoft.com/security**

**RSS 피드**: ✅ 있음
- URL: https://www.microsoft.com/en-us/security/rss
- 보안 관련 게시물
- 업데이트 빈도: 주 1-2회
- 권장 주기: 15분

### 7.2 중복 방지 전략

**방법 1: last_post_id 체크**
```python
def filter_new_posts(posts, last_post_id):
    new_posts = []
    for post in posts:
        if post['id'] == last_post_id:
            break  # 이미 처리한 게시물부터는 건너뛰기
        new_posts.append(post)
    return new_posts
```

**방법 2: Firestore 중복 체크**
```python
async def is_duplicate_post(url):
    query = db.collection('projects').where('source_url', '==', url).limit(1)
    result = await query.get()
    return len(result) > 0
```

### 7.3 Rate Limiting

**제한 사항**:
- 동일 도메인: 1분당 최대 10회
- 전체 크롤링: 동시 5개까지

**구현**:
```python
from slowapi import Limiter

limiter = Limiter(key_func=lambda: "global")

@limiter.limit("10/minute")
async def crawl_site(site_id):
    # 크롤링 로직
    pass
```

---

## 8. 자동화 파이프라인

### 8.1 파이프라인 상세 흐름

```python
class AutoGenerationPipeline:
    """
    완전 자동 카드뉴스 생성 파이프라인
    
    단계:
    1. 게시물 스크래핑
    2. AI 요약 생성
    3. 키워드 추출
    4. 카드뉴스 생성
    5. Firestore 저장
    6. 이메일 알림
    """
    
    async def run(self, post_data: Dict, site_id: str) -> str:
        """
        파이프라인 실행
        
        Args:
            post_data: 크롤링된 게시물 데이터
            site_id: 소스 사이트 ID
            
        Returns:
            project_id: 생성된 프로젝트 ID
        """
        job_id = f"pipeline_{uuid.uuid4()}"
        
        try:
            # Step 1: 게시물 본문 스크래핑
            logger.info(f"[{job_id}] Step 1/6: Scraping post content")
            text = await self.scraper.scrape_url(post_data['url'])
            
            if len(text) < 100:
                raise ValueError("Text too short")
            
            # Step 2: 언어 감지
            logger.info(f"[{job_id}] Step 2/6: Detecting language")
            language = self.summarizer._detect_language(text)
            
            # Step 3: AI 요약
            logger.info(f"[{job_id}] Step 3/6: Generating summary")
            summary_data = await self.summarizer.summarize(
                text=text,
                max_length=200,
                model="gpt-4.1-nano"  # 자동 생성은 가장 빠른 모델 사용
            )
            
            # Step 4: 카드뉴스 생성
            logger.info(f"[{job_id}] Step 4/6: Generating card news")
            sections = await self.card_generator.generate_sections(
                summary=summary_data['summary'],
                original_text=text,
                card_count=summary_data['recommended_cards'],
                model="gpt-4.1-nano"
            )
            
            # Step 5: Firestore 저장
            logger.info(f"[{job_id}] Step 5/6: Saving to Firestore")
            project_id = await self._save_project(
                title=post_data['title'],
                source_url=post_data['url'],
                source_site_id=site_id,
                original_text=text,
                summary=summary_data['summary'],
                keywords=summary_data['keywords'],
                sections=sections,
                language=language,
                status="draft",
                auto_generated=True
            )
            
            # Step 6: 이메일 알림
            logger.info(f"[{job_id}] Step 6/6: Sending email notification")
            await self.email_service.send_card_generated_notification(
                project_id=project_id
            )
            
            logger.info(f"[{job_id}] Pipeline completed successfully")
            return project_id
            
        except Exception as e:
            logger.error(f"[{job_id}] Pipeline failed: {str(e)}")
            
            # 실패 알림
            await self.email_service.send_pipeline_failed_notification(
                post_url=post_data['url'],
                error=str(e)
            )
            
            raise
```

### 8.2 에러 처리 및 재시도

**재시도 전략**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

class AutoGenerationPipeline:
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def scrape_with_retry(self, url):
        """
        재시도 로직이 포함된 스크래핑
        - 최대 3회 시도
        - 대기 시간: 4초, 8초, 10초
        """
        return await self.scraper.scrape_url(url)
```

**에러별 처리**:
| 에러 유형 | 처리 방법 |
|----------|----------|
| 네트워크 타임아웃 | 3회 재시도 |
| 스크래핑 실패 | 다음 주기에 재시도 |
| AI API 실패 | 관리자 알림, 수동 처리 |
| DB 저장 실패 | 5회 재시도, 실패 시 로그 |

---

## 9. UI/UX 설계

### 9.1 메인 대시보드

**레이아웃 (3개 메뉴)**:

```
┌───────────────────────────────────────────────────────────┐
│  CardNews AI Generator                    👤 User [⚙️]    │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  🤖 크롤링   │  │  ✏️ 수동 생성 │  │  📁 프로젝트  │   │
│  │  사이트 설정 │  │              │  │              │   │
│  │              │  │  Phase 1 기능│  │  저장된 항목 │   │
│  │  3개 사이트  │  │              │  │  15개 프로젝트│   │
│  │  활성화 중   │  │              │  │  5개 초안    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                            │
│  📊 최근 활동                                              │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🆕 "New AI Feature" 카드뉴스 생성됨 - 2시간 전    │  │
│  │ 🤖 Microsoft Security 크롤링 완료 - 3시간 전      │  │
│  │ ✅ "Zero-Day Update" 완료 처리됨 - 어제           │  │
│  └────────────────────────────────────────────────────┘  │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

### 9.2 크롤링 사이트 설정 페이지

```
┌───────────────────────────────────────────────────────────┐
│  🤖 크롤링 사이트 설정                  [+ 새 사이트 추가] │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 📝 Microsoft Security Blog                         │  │
│  │ https://www.microsoft.com/en-us/security           │  │
│  │                                                     │  │
│  │ 상태: [🟢 활성화 ▼]   주기: [15분 ▼]              │  │
│  │ 마지막 크롤링: 5분 전  |  다음 예정: 10분 후       │  │
│  │                                                     │  │
│  │ 통계: ✅ 145회 성공 | ❌ 5회 실패 | 📰 23개 게시물│  │
│  │                                                     │  │
│  │ [수동 크롤링] [수정] [삭제]                        │  │
│  └────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 📝 Microsoft Blogs                                 │  │
│  │ https://blogs.microsoft.com/                       │  │
│  │ ...                                                 │  │
│  └────────────────────────────────────────────────────┘  │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

### 9.3 프로젝트 목록 페이지

```
┌───────────────────────────────────────────────────────────┐
│  📁 저장된 프로젝트                        [🔍 검색]       │
├───────────────────────────────────────────────────────────┤
│  [전체] [초안 (5)] [검토중] [완료 (10)]                  │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────┐ │
│  │ 📰 New Zero-Day  │ │ 📰 AI Innovation │ │ 📰 Cloud │ │
│  │                  │ │                  │ │          │ │
│  │ 🆕 NEW           │ │                  │ │          │ │
│  │                  │ │                  │ │          │ │
│  │ 2시간 전         │ │ 어제             │ │ 2일 전   │ │
│  │ Microsoft Security│ │ MS Blogs        │ │ MS News │ │
│  │ [초안] 5 cards   │ │ [완료] 6 cards  │ │ [완료] 4 │ │
│  └──────────────────┘ └──────────────────┘ └──────────┘ │
│                                                            │
│  [더 보기...]                                              │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

### 9.4 프로젝트 상세/수정 페이지

```
┌───────────────────────────────────────────────────────────┐
│  ← 목록으로    📰 New Zero-Day Vulnerability Discovered   │
├───────────────────────────────────────────────────────────┤
│  소스: Microsoft Security Blog                            │
│  URL: https://www.microsoft.com/en-us/security/blog/...   │
│  생성: 2025-10-25 10:35  |  수정: 2025-10-25 11:00       │
│  상태: [초안 ▼]  버전: v1                                 │
│                                                            │
│  [요약 단계로 돌아가기] [카드 수정하기]                    │
├───────────────────────────────────────────────────────────┤
│  📝 요약                                                   │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Microsoft has discovered a new zero-day...         │  │
│  │ ...                                                 │  │
│  └────────────────────────────────────────────────────┘  │
│                                                            │
│  🏷️ 키워드: security, zero-day, vulnerability, patch     │
│                                                            │
│  📄 카드 목록 (5장)                                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 1. [Title] Breaking Security News                  │  │
│  │    Microsoft discovers critical vulnerability...   │  │
│  ├────────────────────────────────────────────────────┤  │
│  │ 2. [Content] What is a Zero-Day?                   │  │
│  │    A zero-day vulnerability is...                  │  │
│  ├────────────────────────────────────────────────────┤  │
│  │ 3. [Content] Impact Analysis                       │  │
│  │ ...                                                 │  │
│  └────────────────────────────────────────────────────┘  │
│                                                            │
│  [삭제] [복사] [내보내기] [완료 처리]                     │
└───────────────────────────────────────────────────────────┘
```

---

## 10. 기술 스택

### 10.1 Backend 추가 라이브러리

```txt
# requirements.txt 추가

# 크롤링
feedparser==6.0.10
playwright==1.40.0

# 스케줄링
APScheduler==3.10.4

# 이메일
sendgrid==6.11.0

# 유틸리티
tenacity==8.2.3  # 재시도 로직
python-dateutil==2.8.2
```

### 10.2 Frontend 추가 라이브러리

```json
// package.json 추가 (필요시)
{
  "dependencies": {
    "react-table": "^7.8.0",  // 프로젝트 목록 테이블
    "date-fns": "^2.30.0"     // 날짜 포맷팅
  }
}
```

### 10.3 인프라

**Render 설정 업데이트**:
- **메모리**: 512MB → **1GB** (크롤링 부하)
- **Background Worker**: 추가 필요 (스케줄러 실행)

**환경 변수 추가**:
```env
# SendGrid
SENDGRID_API_KEY=SG.xxx
ADMIN_EMAIL=admin@example.com

# 크롤링 설정
CRAWL_INTERVAL=15  # 기본 주기 (분)
MAX_CONCURRENT_CRAWLS=5

# Playwright
PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright
```

---

## 11. 개발 일정

### Week 1: 기반 구축 (7일)

| 일차 | 작업 | 산출물 |
|------|------|--------|
| Day 1-2 | Firestore 스키마 설계 및 구현 | 4개 컬렉션 생성 |
| Day 3-4 | 프로젝트 저장 기능 구현 | API 5개 |
| Day 5-7 | 크롤링 사이트 관리 UI/API | 사이트 CRUD 완성 |

**체크포인트 1**:
- [ ] Firestore 스키마 완성
- [ ] 프로젝트 저장/조회 가능
- [ ] 사이트 등록/목록 UI 완성

### Week 2: 크롤링 시스템 (7일)

| 일차 | 작업 | 산출물 |
|------|------|--------|
| Day 8-9 | RSS 파서 구현 | `rss_service.py` |
| Day 10-11 | Playwright 크롤러 구현 | `crawler_service.py` |
| Day 12-14 | APScheduler 통합 및 테스트 | 스케줄러 동작 |

**체크포인트 2**:
- [ ] RSS 피드 파싱 성공
- [ ] Playwright 크롤링 성공
- [ ] 스케줄러 15분마다 자동 실행
- [ ] Microsoft 3개 사이트 크롤링 성공

### Week 3: 자동화 파이프라인 (7일)

| 일차 | 작업 | 산출물 |
|------|------|--------|
| Day 15-17 | 파이프라인 오케스트레이션 | `pipeline_service.py` |
| Day 18-19 | SendGrid 이메일 통합 | `email_service.py` |
| Day 20-21 | 파이프라인 테스트 및 최적화 | End-to-End 동작 |

**체크포인트 3**:
- [ ] 자동 생성 파이프라인 동작
- [ ] 이메일 알림 발송 성공
- [ ] DB 저장 확인
- [ ] 평균 생성 시간 30초 이내

### Week 4: 프로젝트 관리 (7일)

| 일차 | 작업 | 산출물 |
|------|------|--------|
| Day 22-24 | 프로젝트 목록 UI | 목록 페이지 |
| Day 25-26 | 프로젝트 상세/수정 UI | 상세 페이지 |
| Day 27-28 | 메인 대시보드 통합 | 3개 메뉴 완성 |

**체크포인트 4**:
- [ ] 프로젝트 목록 조회 가능
- [ ] 프로젝트 수정 가능 (요약/카드)
- [ ] 메인 대시보드 완성

### Week 5-6: 테스트 및 배포 (14일)

| 일차 | 작업 | 산출물 |
|------|------|--------|
| Day 29-32 | 통합 테스트 | 테스트 케이스 |
| Day 33-35 | 버그 수정 | 안정화 |
| Day 36-38 | 성능 최적화 | 속도 개선 |
| Day 39-42 | 프로덕션 배포 및 모니터링 | 라이브 서비스 |

**최종 체크포인트**:
- [ ] 모든 기능 정상 동작
- [ ] 크롤링 성공률 95% 이상
- [ ] 평균 생성 시간 30초 이내
- [ ] 이메일 발송 성공률 99% 이상
- [ ] 프로덕션 배포 완료

---

## 12. 테스트 계획

### 12.1 단위 테스트

**테스트 대상**:
```python
# tests/test_rss_service.py
def test_parse_rss_feed():
    """RSS 피드 파싱 테스트"""
    pass

# tests/test_crawler_service.py
def test_scrape_website():
    """웹 스크래핑 테스트"""
    pass

# tests/test_pipeline_service.py
def test_auto_generation_pipeline():
    """자동 생성 파이프라인 테스트"""
    pass

# tests/test_email_service.py
def test_send_notification():
    """이메일 발송 테스트 (SendGrid Mock)"""
    pass
```

### 12.2 통합 테스트

**시나리오 1: 전체 자동 생성 흐름**
```
1. 사이트 등록
2. 수동 크롤링 트리거
3. 새 게시물 발견 확인
4. 파이프라인 자동 실행 확인
5. DB 저장 확인
6. 이메일 수신 확인
7. 프로젝트 목록에서 확인
8. 프로젝트 수정
9. 완료 처리
```

**시나리오 2: 스케줄러 동작**
```
1. 사이트 등록 (15분 주기)
2. 15분 대기
3. 자동 크롤링 실행 확인
4. 로그 확인
```

### 12.3 성능 테스트

**목표**:
- 크롤링 1회: 10초 이내
- 파이프라인 전체: 30초 이내
- 동시 크롤링: 5개까지

**도구**: `pytest-benchmark`

---

## 📊 요약

### Phase 2 핵심 포인트

| 항목 | 내용 |
|------|------|
| **목표** | RSS 기반 자동화 카드뉴스 생성 시스템 |
| **타겟 사이트** | RSS 지원 사이트 (Microsoft 블로그 등) |
| **핵심 기능** | RSS 크롤링 → 자동 생성 → 저장 → 이메일 알림 |
| **기술 스택** | RSS Parser (feedparser), APScheduler, SendGrid |
| **개발 기간** | **3-4주** (21-28일) ⚡ 단축! |
| **주요 API** | 12+ 엔드포인트 |
| **데이터베이스** | Firestore 5개 컬렉션 (email_recipients 추가) |
| **메뉴 구성** | 4개 (RSS 설정 / Phase 1 / 프로젝트 / 알림) |

### 성공 기준

- ✅ 크롤링 성공률 95% 이상
- ✅ 자동 생성 성공률 90% 이상
- ✅ 이메일 발송 성공률 99% 이상
- ✅ 평균 처리 시간 30초 이내
- ✅ 사용자 수정 후 최종 저장 가능

---

**이 문서는 Phase 2 개발을 위한 완전한 가이드입니다.**  
**개발 시작 전 팀원들과 함께 검토하고, 필요시 수정하세요.**

**문의**: [GitHub Issues](https://github.com/hyunilhlee/ma-cardnews/issues)

---

**Last Updated**: 2025-10-26 (RSS 전용으로 단순화)

