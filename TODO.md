# CardNews AI Generator - 개발 현황

## ✅ Phase 1 (MVP) - 완료

### 핵심 기능
- [x] **소스 입력**
  - [x] URL 링크 입력
  - [x] 다중 URL 입력 (줄바꿈 구분)
  - [x] 텍스트 직접 입력
  - [x] 입력 가시성 개선 (text-gray-900)
  - [x] URL 입력을 기본 옵션으로 설정

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
  - [x] 3단계 언어 감지 폴백 (auto → ko → en)

- [x] **카드뉴스 생성**
  - [x] AI 기반 자동 생성
  - [x] JSON 형식 구조화
  - [x] 카드 시작 옵션 (제목/내용 선택)
  - [x] 타입별 카드 (title, content, closing)
  - [x] **모든 카드뉴스 한글 생성** (영문 원본도 한글로 번역) ⭐

- [x] **AI 채팅 편집**
  - [x] Function Calling 구현
  - [x] 특정 카드 수정
  - [x] 카드 순서 변경
  - [x] 자연어 전체 수정 (modify_all_content)
    - [x] 톤 변경 (존댓말/반말/전문적/친근하게)
    - [x] 길이 조절 (간결하게/상세하게)
    - [x] 스타일 변경 (스토리텔링/질문형식/리스트)
    - [x] 이모지 추가 등 자유로운 수정
  - [x] **Undo 기능** - 이전 상태로 복원 ⭐

- [x] **UI/UX**
  - [x] Next.js 14 (App Router)
  - [x] Tailwind CSS 스타일링
  - [x] Zustand 상태 관리
  - [x] react-hot-toast 알림
  - [x] OpenAI 연결 상태 표시
  - [x] AI 모델 카드 선택 UI
  - [x] 반응형 디자인
  - [x] 채팅 입력 텍스트 검은색 표시

- [x] **Backend**
  - [x] FastAPI 구조
  - [x] Pydantic 모델
  - [x] Web Scraping (newspaper3k, BeautifulSoup)
  - [x] 다중 URL 스크래핑
  - [x] 언어 자동 감지 (3단계 폴백)
  - [x] CORS 설정 (Vercel 와일드카드)
  - [x] Firebase Firestore 통합
  - [x] 인메모리 fallback
  - [x] 짧은 콘텐츠 에러 처리 (명확한 메시지)

- [x] **배포**
  - [x] Frontend → Vercel
  - [x] Backend → Render
  - [x] 환경 변수 설정
  - [x] GitHub 연동 (자동 배포)

---

## 🎉 Phase 2 (RSS Auto-Generation) - 완료! ✅

### 📅 완료일: 2025-10-28

### 🚀 주요 성과

**100% 자동화 달성!**
- ✅ RSS 피드 자동 크롤링
- ✅ 자동 카드뉴스 생성
- ✅ Firebase Firestore 영구 저장
- ✅ 프로덕션 배포 완료 (Render + Vercel)

### 주요 업데이트

#### 1. RSS 피드 100% 보존 로직 ✅
- 모든 RSS 피드를 프로젝트로 생성 (최소 10자 이상)
- 상태로 진행 단계 구분 (draft/summarized/completed)
- `last_error` 필드로 실패 원인 기록
- **버려지는 피드 없음!**

#### 2. 통계 용어 명확화 ✅
- **RSS 사이트 관리**: "크롤링 횟수", "새 글 발견 (누적)", "카드뉴스 (누적)"
- **크롤링 로그**: "RSS 글 수", "새 글 발견 (이번 크롤링)", "카드뉴스 생성 (이번 크롤링)"
- 사용자 혼란 완전 제거

#### 3. CORS 및 Firebase 초기화 개선 ✅
- localhost 명시적 허용
- Firebase 캐싱 문제 해결
- Firestore 복합 인덱스 우회 (Python 필터링)

#### 4. Pydantic 모델 개선 ✅
- `source_content`를 Optional로 변경
- RSS 자동 생성 프로젝트의 None 값 허용
- 500 에러 해결

#### 5. 프로덕션 배포 완료 ✅
- **Backend**: Render (https://ma-cardnews-api.onrender.com)
- **Frontend**: Vercel (https://frontend-pied-delta-74.vercel.app)
- GitHub 연동으로 자동 배포

### 완료된 기능

#### 1. 데이터베이스 및 저장소 ✅
- [x] **Firebase Firestore 스키마 설계** (4개 컬렉션)
  - [x] `sites` 컬렉션 (크롤링 사이트 관리)
  - [x] `projects` 컬렉션 (생성된 카드뉴스 프로젝트)
  - [x] `crawl_logs` 컬렉션 (크롤링 이력)
  - [x] `rss_posts` 컬렉션 (RSS 게시물 저장) ⭐

- [x] **프로젝트 저장 기능**
  - [x] 프로젝트 생성 및 자동 저장
  - [x] 프로젝트 버전 관리
  - [x] 프로젝트 상태 관리 (draft/summarized/completed)
  - [x] 프로젝트 메타데이터 (생성일, 수정일, 소스 URL)
  - [x] `last_error` 필드로 실패 원인 기록

#### 2. 크롤링 사이트 관리 ✅
- [x] **사이트 등록 UI**
  - [x] 크롤링 사이트 목록 페이지
  - [x] 사이트 추가/삭제 기능
  - [x] RSS 피드 유효성 자동 검증
  - [x] 사이트 활성화/비활성화 토글
  - [x] 통계 표시 (크롤링 횟수, 새 글 발견, 카드뉴스)

- [x] **기본 등록 사이트 (RSS 지원)**
  - [x] https://blogs.microsoft.com/ (RSS: /feed/)
  - [x] https://news.microsoft.com/source/feed
  - [x] https://www.microsoft.com/en-us/security/blog/ (RSS: /feed/)

- [x] **Backend API**
  - [x] `POST /api/sites` - 사이트 등록
  - [x] `GET /api/sites` - 사이트 목록 조회
  - [x] `PUT /api/sites/{site_id}` - 사이트 수정
  - [x] `DELETE /api/sites/{site_id}` - 사이트 삭제
  - [x] `POST /api/sites/validate-rss` - RSS URL 유효성 검사
  - [x] `POST /api/sites/{site_id}/trigger-crawl` - 수동 크롤링 트리거
  - [x] `GET /api/sites/{site_id}/crawl-logs` - 크롤링 로그 조회

#### 3. RSS 기반 자동 크롤링 시스템 ✅
- [x] **RSS 피드 파서**
  - [x] `feedparser` 라이브러리 통합
  - [x] RSS 피드 유효성 검증
  - [x] 새 게시물 자동 감지
  - [x] 발행 시간 기반 필터링
  - [x] RSS 메타데이터 추출 (제목, 날짜, 요약, content)
  - [x] HTML 태그 제거

- [x] **스케줄러 (APScheduler)**
  - [x] APScheduler 통합
  - [x] 사이트별 크롤링 주기 설정 (30분 기본)
  - [x] 재시도 로직 (tenacity)
  - [x] 크롤링 이력 로그 저장
  - [x] 스케줄러 자동 시작/종료

#### 4. 자동 카드뉴스 생성 파이프라인 ✅
- [x] **자동 생성 워크플로우**
  - [x] 새 게시물 감지 → 자동 스크래핑
  - [x] 자동 요약 및 키워드 추출
  - [x] 자동 카드뉴스 생성
  - [x] DB에 상태별 저장 (draft/summarized/completed)
  - [x] **100% 보존 로직**: 모든 RSS 피드를 프로젝트로 생성
  - [x] `last_error` 필드로 실패 원인 기록

- [x] **상태 관리**
  - [x] draft: 내용 짧음 또는 요약 실패
  - [x] summarized: 요약 성공, 카드뉴스 실패
  - [x] completed: 전체 성공

#### 5. 프로젝트 관리 시스템 ✅
- [x] **프로젝트 목록 페이지**
  - [x] 저장된 프로젝트 전체 목록
  - [x] 필터링 (상태별: draft/summarized/completed)
  - [x] 전체 행 클릭하여 편집 페이지 이동
  - [x] 상태 뱃지 표시
  - [x] 프로젝트 삭제 기능
  - [x] 키워드 표시

- [x] **프로젝트 편집 페이지**
  - [x] 프로젝트 정보 (제목, 소스 URL, 생성일, 상태)
  - [x] 카드뉴스 미리보기
  - [x] 키워드 표시
  - [x] **목록으로 버튼 동적 이동** (RSS → Library, 일반 → Projects) ⭐

- [x] **프로젝트 수정 기능**
  - [x] AI 채팅으로 카드 수정
  - [x] 특정 카드 수정
  - [x] 전체 수정 (자연어)
  - [x] 수정 후 저장 (버전 증가)
  - [x] **Undo 기능** - 이전 상태로 복원 ⭐

#### 6. 메인 대시보드 (4개 메뉴) ✅
- [x] **1️⃣ RSS 사이트 설정** (`/sites`)
  - [x] 등록된 RSS 사이트 목록
  - [x] 사이트별 크롤링 통계
  - [x] 새 RSS 사이트 추가/삭제
  - [x] 수동 크롤링 버튼
  - [x] 크롤링 로그 조회 모달

- [x] **2️⃣ 수동 카드뉴스 생성** (`/source`)
  - [x] 기존 Phase 1 UI 그대로 유지
  - [x] URL/텍스트 입력
  - [x] 즉시 생성 및 편집

- [x] **3️⃣ 저장된 프로젝트** (`/projects`)
  - [x] 프로젝트 목록 페이지
  - [x] 상태별 필터링
  - [x] 프로젝트 클릭하여 편집

- [x] **4️⃣ RSS Library** (`/library`) ⭐ Phase 2.5
  - [x] 모든 RSS 게시물 통합 조회
  - [x] 월별 필터링 (2025년 9월부터)
  - [x] 사이트별 필터링
  - [x] 키워드 검색
  - [x] 카드 형태 표시

---

## 🎨 Phase 2.5 (RSS Library & Optimization) - 완료! ✅

### 📅 완료일: 2025-10-28

### 🚀 주요 성과

**RSS Library 및 사용자 경험 대폭 개선!**
- ✅ RSS Library 통합 피드 구축
- ✅ 자동 AI 처리 (한글 번역, 요약, 키워드)
- ✅ 카드뉴스 생성 UX 개선 (로딩 페이지)
- ✅ Undo 기능 추가
- ✅ 모든 카드뉴스 한글 생성

### 완료된 기능

#### 1. RSS Library (통합 피드) ✅
- [x] **RSS Posts 영구 저장**
  - [x] `rss_posts` 컬렉션 생성
  - [x] 모든 RSS 게시물 DB 저장 (30일 이후도 유지)
  - [x] 자동 AI 요약 (8-12문장, 한글)
  - [x] 자동 키워드 추출 (최대 5개, 한글)
  - [x] 제목 한글 번역 (원문 영어 시)
  - [x] 원본 제목 저장 (`title_original`)

- [x] **Library 페이지** (`/library`)
  - [x] 모든 RSS 게시물 최신순 표시
  - [x] 월별 필터링 (2025년 9월부터)
  - [x] 사이트별 필터링
  - [x] 키워드 검색
  - [x] 무한 스크롤 (페이지네이션)

- [x] **Library 카드 UI**
  - [x] 한글 제목 + 원문 제목 (영어) 함께 표시
  - [x] 키워드 태그 표시
  - [x] 실제 날짜/시간 표시 (yyyy년 M월 d일 HH:mm)
  - [x] AI 요약문 표시 (한글, 8-12문장)
  - [x] 카드뉴스 생성 상태 표시 ("✅ 카드뉴스 생성됨")
  - [x] 생성된 카드뉴스는 바로 편집 페이지로 이동

#### 2. 자동 AI 처리 파이프라인 ✅
- [x] **RSS 크롤링 시 자동 처리**
  - [x] 콘텐츠 부족 시 자동 스크래핑
  - [x] AI 요약 생성 (8-12문장, 한글)
  - [x] 키워드 추출 (최대 5개, 한글)
  - [x] 제목 한글 번역 (OpenAI Translation)
  - [x] 모든 데이터 DB 저장

- [x] **기존 RSS 게시물 마이그레이션**
  - [x] `migrate_rss_posts.py` 스크립트 작성
  - [x] 모든 기존 게시물 AI 처리
  - [x] 한글 번역 및 요약 적용
  - [x] 키워드 추출
  - [x] DB 업데이트

#### 3. 카드뉴스 생성 UX 개선 ✅
- [x] **로딩 페이지** (`/generating`)
  - [x] 스피닝 애니메이션
  - [x] 진행 단계 표시 (콘텐츠 분석, AI 요약, 디자인)
  - [x] 자동 리다이렉트 (성공 → 편집, 실패 → Library)

- [x] **직접 생성 플로우**
  - [x] Library에서 "카드뉴스 생성" 클릭 → 바로 생성
  - [x] 요약 페이지 건너뛰기 (RSS는 이미 요약됨)
  - [x] 생성 완료 후 편집 페이지로 이동

- [x] **카드뉴스 상태 관리**
  - [x] RSS Post에 `has_cardnews` 플래그 추가
  - [x] `project_id` 연결
  - [x] 중복 생성 방지

#### 4. 편집 기능 개선 ✅
- [x] **Undo 기능**
  - [x] AI 수정 전 백업 저장
  - [x] "↩️ 이전 상태로 복원하기" 버튼
  - [x] 섹션 전체 복원

- [x] **목록 버튼 동적 이동**
  - [x] RSS 프로젝트 → Library로 이동
  - [x] 일반 프로젝트 → Projects로 이동
  - [x] `source_type` 기반 자동 판단

#### 5. 한글 생성 강화 ✅
- [x] **모든 카드뉴스 한글로 생성**
  - [x] 프롬프트 강화 (한글 우선 지시)
  - [x] 시스템 메시지 강화 (Korean expert)
  - [x] 영문 원본도 한글로 자동 번역
  - [x] 일관된 한글 출력 보장

- [x] **에러 처리 개선**
  - [x] `recommended_card_count` None 처리
  - [x] 짧은 콘텐츠 명확한 에러 메시지
  - [x] 500 에러 방지

#### 6. Backend API 추가 ✅
- [x] **Library API**
  - [x] `GET /api/library/feed` - RSS 통합 피드
  - [x] `POST /api/library/create-cardnews` - Library에서 카드뉴스 생성
  - [x] 월별 필터링 지원
  - [x] 사이트별 필터링 지원
  - [x] 페이지네이션 (limit/offset)

- [x] **RSS Post 관리**
  - [x] `create_rss_post` - RSS 게시물 생성/업데이트
  - [x] `get_rss_post_by_guid` - GUID로 조회
  - [x] `title_original`, `keywords` 필드 추가

#### 7. 외부 라이브러리 추가 ✅
- [x] **Frontend**
  - [x] `date-fns` - 날짜 포맷팅
  - [x] `axios` - HTTP 클라이언트

---

## 🎯 Phase 2.5 개발 통계

- **전체 진행률**: 100% ✅
- **개발 기간**: 2025-10-28 (1일)
- **신규 API**: 2개 엔드포인트
- **신규 페이지**: 2개 (/library, /generating)
- **신규 컬렉션**: 1개 (rss_posts)
- **처리된 RSS 게시물**: 100+ (자동 번역 및 요약)

---

## 🎨 Phase 3 (Authentication, Notification & Design) - 미래 계획

### 계획된 기능

#### 1. 사용자 인증 및 관리 🆕
- [ ] **Firebase Authentication**
  - [ ] 이메일/비밀번호 로그인
  - [ ] Google 소셜 로그인
  - [ ] GitHub 소셜 로그인
- [ ] **사용자 프로필**
  - [ ] 프로필 페이지
  - [ ] 사용자별 프로젝트 관리
  - [ ] 권한 관리
- [ ] **대시보드 접근 제어**
  - [ ] 로그인 필수 페이지
  - [ ] 비로그인 시 랜딩 페이지

#### 2. 이메일 알림 시스템 🆕
- [ ] **이메일 등록 관리**
  - [ ] 대시보드에 "알림 설정" 메뉴 추가
  - [ ] 이메일 주소 등록/수정/삭제
  - [ ] 여러 이메일 주소 등록 (최대 5개)
  - [ ] 개별 알림 ON/OFF 토글
  - [ ] 테스트 이메일 발송
- [ ] **SendGrid 통합**
  - [ ] SendGrid API 설정
  - [ ] HTML 이메일 템플릿
  - [ ] 카드뉴스 생성 완료 알림
  - [ ] 크롤링 실패 알림
  - [ ] 주간 요약 리포트
- [ ] **Firestore 컬렉션**
  - [ ] `email_recipients` 컬렉션
  - [ ] `notifications` 컬렉션

#### 3. 웹 스크래핑 시스템 (RSS 없는 사이트)
- [ ] **Playwright 통합**
  - [ ] Playwright 설치 및 설정
  - [ ] JavaScript 렌더링 지원
  - [ ] 헤드리스 브라우저 모드
- [ ] **사이트별 커스텀 크롤링**
  - [ ] 사이트 구조 분석 툴
  - [ ] CSS 셀렉터 설정 UI
  - [ ] 커스텀 스크래핑 로직 저장
- [ ] **크롤링 타입 선택**
  - [ ] 사이트 등록 시 "RSS" 또는 "웹 스크래핑" 선택
  - [ ] 자동 감지 및 추천

#### 4. 디자인 시스템
- [ ] **디자인 템플릿 라이브러리**
  - [ ] 10+ 프리셋 템플릿
  - [ ] 색상 팔레트 선택
  - [ ] 폰트 선택 (한글/영문)
  - [ ] 레이아웃 타입 (중앙/좌/우 정렬)
- [ ] **실시간 미리보기**
- [ ] **커스텀 CSS 지원**

#### 5. 이미지 생성 및 편집
- [ ] AI 이미지 생성 (DALL-E, Midjourney)
- [ ] 이미지 업로드
- [ ] 이미지 편집 (크롭, 필터, 텍스트 오버레이)
- [ ] Unsplash 연동 (무료 이미지)

#### 6. 카드뉴스 내보내기
- [ ] PNG/JPG 이미지로 내보내기 (카드별)
- [ ] PDF로 내보내기 (전체)
- [ ] 고해상도 옵션
- [ ] SNS 최적화 사이즈 (인스타그램, 페이스북 등)

#### 7. 고급 기능
- [ ] 버전 히스토리 고도화
- [ ] 협업 기능 (공유, 댓글)
- [ ] 템플릿 마켓플레이스
- [ ] 분석 대시보드 (조회수, 공유수)

---

## 🐛 알려진 이슈 및 개선 사항

### 버그
- 없음 (현재 알려진 버그 없음)

### 개선 예정
- [ ] Firestore 복합 인덱스 생성 (크롤링 로그 필터링 최적화)
- [ ] 카드 생성 속도 최적화 (스트리밍 응답)
- [ ] 더 많은 언어 지원 (중국어, 스페인어, 프랑스어)
- [ ] 고급 언어 감지 라이브러리 (`langdetect`)
- [ ] WebSocket 실시간 채팅
- [ ] 카드 개수 동적 조절 (AI 채팅으로)
- [ ] APScheduler 비동기 실행 개선

---

## 📈 개발 통계

### Phase 1 완료 현황
- **전체 진행률**: 100% ✅
- **핵심 기능**: 8/8 완료
- **배포**: 2/2 완료 (Vercel + Render)

### Phase 2 완료 현황
- **전체 진행률**: 100% ✅
- **개발 기간**: 3일 (2025-10-25 ~ 2025-10-28)
- **핵심 기능**: 9/9 완료
- **신규 API**: 10개 엔드포인트
- **컬렉션**: 3개 (sites, projects, crawl_logs)
- **배포**: 2/2 완료 (Render + Vercel)

### Phase 2.5 완료 현황
- **전체 진행률**: 100% ✅
- **개발 기간**: 1일 (2025-10-28)
- **핵심 기능**: 7/7 완료
- **신규 API**: 2개 엔드포인트
- **신규 페이지**: 2개 (Library, Generating)
- **컬렉션**: 4개 (sites, projects, crawl_logs, rss_posts)
- **배포**: 2/2 완료 (Render + Vercel)

### 코드 통계
- **Backend**: Python, FastAPI, 25+ 파일
- **Frontend**: TypeScript, Next.js, 35+ 컴포넌트
- **테스트**: pytest (백엔드 유닛 테스트)
- **총 커밋**: 120+ commits

---

## 🔗 관련 문서

- **프로젝트 소개**: [README.md](README.md)
- **제품 기획서**: [docs/PRD.md](docs/PRD.md)
- **개발 문서**: [docs/개발문서.md](docs/개발문서.md)
- **Phase 2 개발 정의서**: [PHASE2_SPEC.md](PHASE2_SPEC.md)
- **Phase 2 완료 보고서**: [docs/PHASE2_COMPLETE.md](docs/PHASE2_COMPLETE.md)
- **Phase 2.5 개발 정의서**: [PHASE2_5_SPEC.md](PHASE2_5_SPEC.md)
- **Phase 2.5 완료 보고서**: [docs/PHASE2_5_COMPLETE.md](docs/PHASE2_5_COMPLETE.md) 🆕

---

## 🎯 다음 단계: Phase 3

Phase 2.5가 성공적으로 완료되었습니다! 🎉

다음 단계:
- **Phase 3**: 인증, 알림, 디자인 시스템 추가

---

**Last Updated**: 2025-10-28
