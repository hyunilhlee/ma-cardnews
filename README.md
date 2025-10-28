# 📰 CardNews AI Generator

AI 기반 카드뉴스 자동 생성 서비스 (Phase 2.5 완료! 🎉)

## 🎯 프로젝트 개요

링크 또는 텍스트를 입력하면 AI가 자동으로 카드뉴스를 생성하고, 자연어로 대화하며 내용을 수정할 수 있는 웹 서비스입니다.

**Phase 2.5 완료**: RSS Library 및 사용자 경험 대폭 개선! (2025-10-28)

### 주요 기능

#### Phase 1 (MVP) ✅
- ✅ **다중 URL 입력**: 여러 URL을 한번에 입력하여 통합 카드뉴스 생성
- ✅ **다국어 지원**: 영어/한국어/일본어 자동 감지 및 처리
- ✅ **AI 자동 요약**: GPT-4.1/GPT-5 시리즈를 활용한 핵심 내용 추출
- ✅ **자연어 편집**: "전체를 존댓말로 바꿔줘" 같은 자연어 명령으로 쉽게 수정
- ✅ **AI 모델 선택**: 4가지 모델 중 선택 가능 (속도/품질/비용 균형)
- ✅ **Undo 기능**: AI 수정 후 이전 상태로 복원 가능

#### Phase 2 (RSS Auto-Generation) ✅
- ✅ **RSS 자동 크롤링**: 등록된 RSS 사이트 자동 모니터링 (기본 30분 주기)
- ✅ **자동 카드뉴스 생성**: 새 게시물 발견 시 자동 생성
- ✅ **100% 피드 보존**: 모든 RSS 피드를 프로젝트로 저장 (draft/summarized/completed)
- ✅ **프로젝트 관리**: 저장된 프로젝트 조회, 수정, 삭제
- ✅ **크롤링 통계**: 사이트별 크롤링 횟수, 새 글 발견, 카드뉴스 생성 통계

#### Phase 2.5 (RSS Library & UX Improvements) ✅ 신규!
- ✅ **RSS Library**: 모든 RSS 게시물 통합 조회 (월별/사이트별 필터링)
- ✅ **자동 AI 처리**: RSS 크롤링 시 자동 번역, 요약, 키워드 추출
- ✅ **한글 생성 강화**: 모든 카드뉴스를 한글로 생성 (영문 원본도 자동 번역)
- ✅ **로딩 페이지**: 카드뉴스 생성 진행 상태 표시
- ✅ **키워드 태그**: RSS 게시물 및 프로젝트에 키워드 표시
- ✅ **날짜/시간 표시**: 실제 게시 날짜 및 시간 표시

## 🛠️ 기술 스택

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 3.4
- **State Management**: Zustand 4.4
- **HTTP Client**: Axios
- **Date Formatting**: date-fns
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI 0.104 (Python 3.11+)
- **Database**: Firebase Firestore
- **AI**: OpenAI (GPT-4.1-nano, GPT-4.1-mini, GPT-5-nano, GPT-5-mini)
- **Web Scraping**: newspaper3k, BeautifulSoup4
- **RSS**: feedparser 6.0.11
- **Scheduling**: APScheduler 3.10.4
- **Deployment**: Render (Docker)

## 🚀 빠른 시작

### 1. 환경 변수 설정

**Backend** (`backend/.env`):
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-nano
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=path/to/serviceAccountKey.json
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. 백엔드 실행

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 3. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

### 4. 접속

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 프로젝트 구조

```
CardNews/
├── backend/          # FastAPI 백엔드
│   ├── app/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── models/       # Pydantic 모델
│   │   ├── services/     # 비즈니스 로직
│   │   ├── routers/      # API 라우터
│   │   └── utils/        # 유틸리티
│   ├── requirements.txt
│   └── migrate_rss_posts.py
│
├── frontend/         # Next.js 프론트엔드
│   ├── app/          # Pages (App Router)
│   ├── components/   # React 컴포넌트
│   ├── lib/          # 유틸리티 및 API
│   └── package.json
│
├── docs/             # 상세 문서
│   ├── PRD.md        # 제품 기획서
│   ├── 개발문서.md    # 개발 가이드
│   ├── PHASE2_COMPLETE.md
│   └── PHASE2_5_COMPLETE.md
│
├── PHASE2_SPEC.md    # Phase 2 개발 정의서
├── PHASE2_5_SPEC.md  # Phase 2.5 개발 정의서
├── README.md         # 프로젝트 소개 (이 파일)
└── TODO.md           # 진행 상황 및 체크리스트
```

## 🌐 배포된 서비스

- **Frontend**: https://frontend-pied-delta-74.vercel.app
- **Backend API**: https://ma-cardnews-api.onrender.com

## 📚 문서

- **제품 기획서 (PRD)**: [`docs/PRD.md`](docs/PRD.md)
- **개발 문서**: [`docs/개발문서.md`](docs/개발문서.md)
- **진행 상황**: [`TODO.md`](TODO.md)
- **Phase 2 개발 정의서**: [`PHASE2_SPEC.md`](PHASE2_SPEC.md)
- **Phase 2 완료 보고서**: [`docs/PHASE2_COMPLETE.md`](docs/PHASE2_COMPLETE.md)
- **Phase 2.5 개발 정의서**: [`PHASE2_5_SPEC.md`](PHASE2_5_SPEC.md)
- **Phase 2.5 완료 보고서**: [`docs/PHASE2_5_COMPLETE.md`](docs/PHASE2_5_COMPLETE.md) 🆕

## 🎨 주요 특징

### 1️⃣ RSS Library (신규!)
등록된 모든 RSS 사이트의 게시물을 하나의 통합 피드로 제공합니다.
- **월별 필터링**: 2025년 9월부터 월별로 게시물 조회
- **사이트별 필터링**: 특정 RSS 사이트만 선택하여 조회
- **키워드 검색**: 제목, 요약, 키워드 기반 검색
- **자동 한글 번역**: 영문 제목/요약 자동 번역
- **키워드 태그**: AI가 추출한 키워드 표시

### 2️⃣ 다중 URL 입력
여러 개의 URL을 줄바꿈으로 구분하여 입력하면 자동으로 통합된 카드뉴스를 생성합니다.

### 3️⃣ AI 모델 선택
| 모델 | 속도 | 품질 | 가격 | 추천 |
|------|------|------|------|------|
| GPT-4.1 Nano | 빠름 | 좋음 | 저렴 | ✅ 기본 |
| GPT-4.1 Mini | 빠름 | 좋음 | 보통 | |
| GPT-5 Nano | 빠름 | 더 좋음 | 보통 | |
| GPT-5 Mini | 보통 | 더 좋음 | 높음 | |

### 4️⃣ 자연어 편집 + Undo
```
"전체를 존댓말로 바꿔줘"
"전체를 더 전문적으로 만들어줘"
"전체에 이모지를 추가해줘"
"전체를 간결하게 줄여줘"
```
AI 수정 후 마음에 들지 않으면 "↩️ 이전 상태로 복원하기" 버튼으로 되돌릴 수 있습니다.

### 5️⃣ 한글 생성 강화
모든 카드뉴스가 한글로 생성됩니다. 영문 원본도 자동으로 한글로 번역하여 생성합니다.

## 🔧 개발 현황

### Phase 1 (MVP) - ✅ 완료
- [x] 소스 입력 (URL/텍스트)
- [x] AI 요약 및 키워드 추출
- [x] 카드뉴스 자동 생성
- [x] AI 채팅을 통한 자연어 편집
- [x] 다중 URL 지원
- [x] 다국어 지원
- [x] AI 모델 선택
- [x] 프로덕션 배포 (Vercel + Render)

### Phase 2 (RSS Auto-Generation) - ✅ 완료! (2025-10-28)
- [x] RSS 자동 크롤링 시스템
- [x] 자동 카드뉴스 생성 파이프라인
- [x] Firebase Firestore 통합 (4개 컬렉션)
- [x] 프로젝트 관리 시스템 (CRUD)
- [x] RSS 사이트 관리 UI
- [x] 크롤링 통계 및 로그
- [x] 100% 피드 보존 로직
- [x] 프로덕션 배포 (Render + Vercel)

**개발 기간**: 3일 (2025-10-25 ~ 2025-10-28)

### Phase 2.5 (RSS Library & UX) - ✅ 완료! (2025-10-28)
- [x] RSS Library 통합 피드
- [x] 자동 AI 처리 (번역, 요약, 키워드)
- [x] 월별/사이트별 필터링
- [x] 키워드 검색 및 태그 표시
- [x] 카드뉴스 생성 로딩 페이지
- [x] Undo 기능 (AI 수정 복원)
- [x] 한글 생성 강화
- [x] 목록 버튼 동적 이동
- [x] 날짜/시간 표시

**개발 기간**: 1일 (2025-10-28)

### Phase 3 (Authentication, Notification & Design) - 🔜 예정
- [ ] 사용자 인증 (Firebase Authentication)
- [ ] 이메일 알림 시스템 (SendGrid)
- [ ] 웹 스크래핑 (Playwright)
- [ ] 디자인 템플릿 선택
- [ ] 이미지 생성 및 편집
- [ ] 카드뉴스 이미지 내보내기 (PNG, PDF)
- [ ] 팀 협업 기능

## 📊 프로젝트 통계

- **전체 개발 기간**: 4일 (2025-10-25 ~ 2025-10-28)
- **Phase 1**: 완료 (100%)
- **Phase 2**: 완료 (100%)
- **Phase 2.5**: 완료 (100%)
- **총 커밋**: 120+ commits
- **Backend 파일**: 25+ files
- **Frontend 컴포넌트**: 35+ components
- **API 엔드포인트**: 20+ endpoints
- **컬렉션**: 4개 (sites, projects, crawl_logs, rss_posts)

## 📄 라이선스

MIT License

## 👤 작성자

Hyunil Lee

---

**Note**: 이 프로젝트는 Phase 2.5 (RSS Library & UX)까지 완료된 상태입니다. 

- **Phase 1**: 수동 카드뉴스 생성 (URL/텍스트 입력) ✅
- **Phase 2**: RSS 자동 크롤링 및 카드뉴스 생성 ✅
- **Phase 2.5**: RSS Library 및 사용자 경험 개선 ✅ ← 🆕 완료!
- **Phase 3**: 인증, 알림, 디자인 시스템 (예정)

상세한 개발 가이드는 [`docs/개발문서.md`](docs/개발문서.md)를, Phase 2.5 완료 보고서는 [`docs/PHASE2_5_COMPLETE.md`](docs/PHASE2_5_COMPLETE.md)를 참고하세요.
