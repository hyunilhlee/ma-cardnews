# CardNews AI Generator - 개발 현황

## ✅ Phase 1 (MVP) - 완료

### 핵심 기능
- [x] **소스 입력**
  - [x] URL 링크 입력
  - [x] 다중 URL 입력 (줄바꿈 구분)
  - [x] 텍스트 직접 입력
  - [x] 입력 가시성 개선 (text-gray-900)

- [x] **AI 처리**
  - [x] OpenAI API 통합
  - [x] AI 모델 선택 (4개 모델)
    - [x] GPT-4.1 Nano (기본)
    - [x] GPT-4.1 Mini
    - [x] GPT-5 Nano
    - [x] GPT-5 Mini
  - [x] 텍스트 요약 생성
  - [x] 키워드 자동 추출
  - [x] 추천 카드 수 계산
  - [x] 다국어 지원 (영어/한국어/일본어)

- [x] **카드뉴스 생성**
  - [x] AI 기반 자동 생성
  - [x] JSON 형식 구조화
  - [x] 카드 시작 옵션 (제목/내용 선택)
  - [x] 타입별 카드 (title, content, closing)
  - [x] 다국어 콘텐츠 생성

- [x] **AI 채팅 편집**
  - [x] Function Calling 구현
  - [x] 특정 카드 수정
  - [x] 카드 순서 변경
  - [x] 자연어 전체 수정 (modify_all_content)
    - [x] 톤 변경 (존댓말/반말/전문적/친근하게)
    - [x] 길이 조절 (간결하게/상세하게)
    - [x] 스타일 변경 (스토리텔링/질문형식/리스트)
    - [x] 이모지 추가 등 자유로운 수정

- [x] **UI/UX**
  - [x] Next.js 14 (App Router)
  - [x] Tailwind CSS 스타일링
  - [x] Zustand 상태 관리
  - [x] react-hot-toast 알림
  - [x] OpenAI 연결 상태 표시
  - [x] AI 모델 카드 선택 UI
  - [x] 반응형 디자인

- [x] **Backend**
  - [x] FastAPI 구조
  - [x] Pydantic 모델
  - [x] Web Scraping (newspaper3k, BeautifulSoup)
  - [x] 다중 URL 스크래핑
  - [x] 언어 자동 감지
  - [x] CORS 설정 (Vercel 와일드카드)
  - [x] Firebase Firestore 통합
  - [x] 인메모리 fallback

- [x] **배포**
  - [x] Frontend → Vercel
  - [x] Backend → Render
  - [x] 환경 변수 설정
  - [x] GitHub Actions (자동 배포)

---

## 🚧 Phase 2 (Auto-Generation) - 진행 예정 🆕

### 개요
**사용자가 사이트를 등록하면 자동으로 새 게시물을 감지하고 카드뉴스를 생성하는 완전 자동화 시스템**

### 핵심 목표
- ✨ **100% 자동화**: 수동 입력 없이 자동으로 카드뉴스 생성
- 🤖 **지능형 크롤링**: RSS 피드 및 크롤링봇으로 새 게시물 자동 감지
- 💾 **영구 저장**: 모든 프로젝트를 DB에 저장하고 관리
- 📧 **알림 시스템**: 카드뉴스 생성 완료 시 이메일 알림
- 🎯 **Microsoft 블로그 타겟**: 3개 Microsoft 사이트 자동 모니터링

### 1. 데이터베이스 및 저장소
- [ ] **Firebase Firestore 스키마 설계**
  - [ ] `sites` 컬렉션 (크롤링 사이트 관리)
  - [ ] `projects` 컬렉션 (생성된 카드뉴스 프로젝트)
  - [ ] `crawl_logs` 컬렉션 (크롤링 이력)
  - [ ] `notifications` 컬렉션 (알림 이력)

- [ ] **프로젝트 저장 기능**
  - [ ] 프로젝트 생성 및 자동 저장
  - [ ] 프로젝트 버전 관리
  - [ ] 프로젝트 상태 관리 (초안/검토중/완료)
  - [ ] 프로젝트 메타데이터 (생성일, 수정일, 소스 URL)

### 2. 크롤링 사이트 관리
- [ ] **사이트 등록 UI**
  - [ ] 크롤링 사이트 목록 페이지
  - [ ] 사이트 추가 폼 (URL, 이름, 설명, 크롤링 주기)
  - [ ] 사이트 수정/삭제 기능
  - [ ] 사이트 활성화/비활성화 토글

- [ ] **기본 등록 사이트 (Microsoft)**
  - [ ] https://blogs.microsoft.com/
  - [ ] https://news.microsoft.com/source/asia/region/korea/?lang=ko
  - [ ] https://www.microsoft.com/en-us/security

- [ ] **Backend API**
  - [ ] `POST /api/sites` - 사이트 등록
  - [ ] `GET /api/sites` - 사이트 목록 조회
  - [ ] `PUT /api/sites/{site_id}` - 사이트 수정
  - [ ] `DELETE /api/sites/{site_id}` - 사이트 삭제
  - [ ] `GET /api/sites/{site_id}/status` - 크롤링 상태 확인

### 3. 자동 크롤링 시스템
- [ ] **RSS 피드 파서**
  - [ ] `feedparser` 라이브러리 통합
  - [ ] RSS 피드 자동 감지
  - [ ] 새 게시물 감지 로직
  - [ ] 중복 게시물 필터링

- [ ] **크롤링 봇**
  - [ ] Selenium/Playwright 통합 (JavaScript 렌더링)
  - [ ] 사이트별 커스텀 크롤링 로직
  - [ ] 게시물 본문 추출
  - [ ] 이미지 URL 추출 (Phase 3 대비)

- [ ] **스케줄러 (Cron Job)**
  - [ ] APScheduler 통합
  - [ ] 사이트별 크롤링 주기 설정 (5분/15분/30분/1시간)
  - [ ] 크롤링 실패 시 재시도 로직
  - [ ] 크롤링 이력 로그 저장

### 4. 자동 카드뉴스 생성 파이프라인
- [ ] **자동 생성 워크플로우**
  - [ ] 새 게시물 감지 → 자동 스크래핑
  - [ ] 자동 요약 및 키워드 추출
  - [ ] 자동 카드뉴스 생성 (기본 설정 사용)
  - [ ] DB에 "초안" 상태로 저장
  - [ ] 사용자 이메일 알림 발송

- [ ] **Backend 파이프라인 API**
  - [ ] `POST /api/pipeline/trigger` - 수동 파이프라인 트리거
  - [ ] `GET /api/pipeline/status/{job_id}` - 파이프라인 상태 확인
  - [ ] `GET /api/pipeline/history` - 파이프라인 실행 이력

### 5. 이메일 알림 시스템
- [ ] **이메일 서비스 통합**
  - [ ] SendGrid API 통합
  - [ ] 이메일 템플릿 작성 (HTML)
  - [ ] 알림 타입별 템플릿
    - [ ] 카드뉴스 생성 완료
    - [ ] 크롤링 실패 알림
    - [ ] 주간 요약 리포트

- [ ] **알림 설정**
  - [ ] 사용자별 알림 설정 UI
  - [ ] 알림 ON/OFF 토글
  - [ ] 알림 수신 이메일 주소 설정

### 6. 프로젝트 관리 시스템
- [ ] **프로젝트 목록 페이지**
  - [ ] 저장된 프로젝트 전체 목록
  - [ ] 필터링 (상태별, 날짜별, 소스별)
  - [ ] 검색 기능 (제목, 키워드)
  - [ ] 페이지네이션
  - [ ] 썸네일 미리보기

- [ ] **프로젝트 상세 페이지**
  - [ ] 프로젝트 정보 (제목, 소스 URL, 생성일, 상태)
  - [ ] 카드뉴스 미리보기
  - [ ] 수정 모드 진입 (요약 단계/카드 단계 선택)
  - [ ] 버전 히스토리

- [ ] **프로젝트 수정 기능**
  - [ ] **요약 단계로 돌아가기**
    - [ ] 요약문 수정
    - [ ] 키워드 재선택
    - [ ] 카드 수 조정
    - [ ] 재생성 버튼
  - [ ] **카드 단계 수정**
    - [ ] 기존 AI 채팅 기능 활용
    - [ ] 특정 카드 수정
    - [ ] 전체 수정 (자연어)
  - [ ] 수정 후 저장 (새 버전 생성)
  - [ ] "완료" 상태로 변경

- [ ] **프로젝트 삭제**
  - [ ] 소프트 삭제 (archived 상태)
  - [ ] 영구 삭제 옵션

### 7. 메인 대시보드 (3개 메뉴)
- [ ] **1️⃣ 크롤링 사이트 설정**
  - [ ] 등록된 사이트 목록
  - [ ] 사이트별 크롤링 상태 (마지막 크롤링 시간, 다음 예정 시간)
  - [ ] 새 사이트 추가 버튼
  - [ ] 사이트별 빠른 수동 크롤링 버튼

- [ ] **2️⃣ 수동 카드뉴스 생성 (Phase 1 기능)**
  - [ ] 기존 Phase 1 UI 그대로 유지
  - [ ] URL/텍스트 입력
  - [ ] 즉시 생성 및 편집

- [ ] **3️⃣ 저장된 프로젝트**
  - [ ] 프로젝트 카드 그리드
  - [ ] 상태별 탭 (초안/검토중/완료)
  - [ ] 최근 프로젝트 우선 표시
  - [ ] "새로 생성됨" 뱃지

### 8. Backend 추가 개발
- [ ] **Pydantic 모델 확장**
  - [ ] `Site` 모델 (크롤링 사이트)
  - [ ] `CrawlLog` 모델 (크롤링 이력)
  - [ ] `Notification` 모델 (알림)
  - [ ] `Project` 모델 확장 (버전, 상태, 메타데이터)

- [ ] **새 서비스 구현**
  - [ ] `crawler_service.py` - 크롤링 로직
  - [ ] `rss_service.py` - RSS 피드 파싱
  - [ ] `scheduler_service.py` - 스케줄링
  - [ ] `email_service.py` - 이메일 발송
  - [ ] `pipeline_service.py` - 자동 생성 파이프라인

- [ ] **새 라우터 추가**
  - [ ] `sites.py` - 사이트 관리 API
  - [ ] `pipeline.py` - 파이프라인 API
  - [ ] `notifications.py` - 알림 API

### 9. 외부 라이브러리 추가
- [ ] **Python (Backend)**
  - [ ] `feedparser` - RSS 파싱
  - [ ] `APScheduler` - 스케줄링
  - [ ] `sendgrid` - 이메일 발송
  - [ ] `playwright` - JavaScript 렌더링 크롤링
  - [ ] `selenium` - 대체 크롤링 옵션

- [ ] **Frontend**
  - [ ] 추가 라이브러리 필요시 검토

### 10. 배포 및 인프라
- [ ] **환경 변수 추가**
  - [ ] `SENDGRID_API_KEY`
  - [ ] `ADMIN_EMAIL`
  - [ ] `CRAWL_INTERVAL` (기본 크롤링 주기)
  - [ ] `MAX_CONCURRENT_CRAWLS`

- [ ] **Render 설정 업데이트**
  - [ ] Cron Job 또는 Background Worker 설정
  - [ ] 메모리 증가 (크롤링 부하)

---

## 🎨 Phase 3 (Design & Export) - 미래 계획

### 계획된 기능 (기존 Phase 2에서 이동)

#### 1. 디자인 시스템
- [ ] 디자인 템플릿 라이브러리
  - [ ] 10+ 프리셋 템플릿
  - [ ] 색상 팔레트 선택
  - [ ] 폰트 선택 (한글/영문)
  - [ ] 레이아웃 타입 (중앙/좌/우 정렬)
- [ ] 실시간 미리보기
- [ ] 커스텀 CSS 지원

#### 2. 이미지 생성 및 편집
- [ ] AI 이미지 생성 (DALL-E, Midjourney)
- [ ] 이미지 업로드
- [ ] 이미지 편집 (크롭, 필터, 텍스트 오버레이)
- [ ] Unsplash 연동 (무료 이미지)

#### 3. 카드뉴스 내보내기
- [ ] PNG/JPG 이미지로 내보내기 (카드별)
- [ ] PDF로 내보내기 (전체)
- [ ] 고해상도 옵션
- [ ] SNS 최적화 사이즈 (인스타그램, 페이스북 등)

#### 4. 사용자 인증 및 관리
- [ ] Firebase Authentication
  - [ ] 이메일/비밀번호
  - [ ] Google 로그인
  - [ ] GitHub 로그인
- [ ] 사용자 프로필
- [ ] 팀 협업 기능
- [ ] 권한 관리

#### 5. 고급 기능
- [ ] 버전 히스토리 고도화
- [ ] 협업 기능 (공유, 댓글)
- [ ] 템플릿 마켓플레이스
- [ ] 분석 대시보드 (조회수, 공유수)

---

## 🐛 알려진 이슈 및 개선 사항

### 버그
- 없음 (현재 알려진 버그 없음)

### 개선 예정
- [ ] 카드 생성 속도 최적화 (스트리밍 응답)
- [ ] 더 많은 언어 지원 (중국어, 스페인어, 프랑스어)
- [ ] 고급 언어 감지 라이브러리 (`langdetect`)
- [ ] WebSocket 실시간 채팅
- [ ] 카드 개수 동적 조절 (AI 채팅으로)

---

## 📈 개발 통계

### Phase 1 완료 현황
- **전체 진행률**: 100% ✅
- **핵심 기능**: 8/8 완료
- **배포**: 2/2 완료 (Vercel + Render)

### Phase 2 계획
- **예상 기간**: 4-6주
- **핵심 기능**: 10개 영역
- **신규 API**: 15+ 엔드포인트
- **타겟 사이트**: 3개 (Microsoft 블로그)

### 코드 통계
- **Backend**: Python, FastAPI, 12개 파일
- **Frontend**: TypeScript, Next.js, 25개+ 컴포넌트
- **테스트**: pytest (백엔드 유닛 테스트)

---

## 🎯 Phase 2 개발 우선순위

### Week 1-2: 기반 구축
1. Firebase Firestore 스키마 설계 및 구축
2. 프로젝트 저장 기능 구현
3. 크롤링 사이트 관리 UI 및 API

### Week 3-4: 크롤링 시스템
1. RSS 피드 파서 구현
2. 크롤링 봇 구현 (Playwright)
3. 스케줄러 설정 (APScheduler)
4. Microsoft 사이트 3개 크롤링 테스트

### Week 5-6: 자동화 파이프라인
1. 자동 생성 파이프라인 구현
2. 이메일 알림 시스템 (SendGrid)
3. 프로젝트 관리 시스템 (목록/상세/수정)
4. 메인 대시보드 UI (3개 메뉴)

### Week 7: 테스트 및 배포
1. 통합 테스트
2. 성능 최적화
3. 프로덕션 배포
4. 문서화 완료

---

## 📝 최근 업데이트

### 2025-10-25
- ✅ Phase 구조 재정의
- ✅ Phase 2를 "Auto-Generation"으로 변경
- ✅ Phase 3로 기존 Phase 2 기능 이동
- ✅ Microsoft 블로그 크롤링 계획 수립

---

## 🔗 관련 문서

- **프로젝트 소개**: [README.md](README.md)
- **제품 기획서**: [docs/PRD.md](docs/PRD.md)
- **개발 문서**: [docs/개발문서.md](docs/개발문서.md)
- **Phase 2 개발 정의서**: [PHASE2_SPEC.md](PHASE2_SPEC.md) 📌 신규

---

**Last Updated**: 2025-10-25
