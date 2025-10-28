# 📰 CardNews AI Generator

AI 기반 카드뉴스 자동 생성 서비스 (Phase 2 완료! 🎉)

## 🎯 프로젝트 개요

링크 또는 텍스트를 입력하면 AI가 자동으로 카드뉴스를 생성하고, 자연어로 대화하며 내용을 수정할 수 있는 웹 서비스입니다.

**Phase 2 완료**: RSS 피드를 통한 자동 카드뉴스 생성 시스템 구축 완료! (2025-10-28)

### 주요 기능

#### Phase 1 (MVP) ✅
- ✅ **다중 URL 입력**: 여러 URL을 한번에 입력하여 통합 카드뉴스 생성
- ✅ **다국어 지원**: 영어/한국어/일본어 자동 감지 및 처리
- ✅ **AI 자동 요약**: GPT-4.1/GPT-5 시리즈를 활용한 핵심 내용 추출
- ✅ **자연어 편집**: "전체를 존댓말로 바꿔줘" 같은 자연어 명령으로 쉽게 수정
- ✅ **AI 모델 선택**: 4가지 모델 중 선택 가능 (속도/품질/비용 균형)

#### Phase 2 (RSS Auto-Generation) ✅ 신규!
- ✅ **RSS 자동 크롤링**: 등록된 RSS 사이트 자동 모니터링 (기본 30분 주기)
- ✅ **자동 카드뉴스 생성**: 새 게시물 발견 시 자동 생성
- ✅ **100% 피드 보존**: 모든 RSS 피드를 프로젝트로 저장 (draft/summarized/completed)
- ✅ **프로젝트 관리**: 저장된 프로젝트 조회, 수정, 삭제
- ✅ **크롤링 통계**: 사이트별 크롤링 횟수, 새 글 발견, 카드뉴스 생성 통계

## 🛠️ 기술 스택

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI (Python 3.11+)
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
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 2. 백엔드 실행

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
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
│   │   ├── models/
│   │   ├── services/
│   │   ├── routers/
│   │   └── utils/
│   └── requirements.txt
│
├── frontend/         # Next.js 프론트엔드
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
│
├── docs/             # 상세 문서
│   ├── PRD.md        # 제품 기획서
│   └── 개발문서.md    # 개발 가이드
│
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
- **Phase 2 완료 보고서**: [`docs/PHASE2_COMPLETE.md`](docs/PHASE2_COMPLETE.md) 🆕

## 🎨 주요 특징

### 1️⃣ 다중 URL 입력
여러 개의 URL을 줄바꿈으로 구분하여 입력하면 자동으로 통합된 카드뉴스를 생성합니다.

### 2️⃣ AI 모델 선택
| 모델 | 속도 | 품질 | 가격 | 추천 |
|------|------|------|------|------|
| GPT-4.1 Nano | 빠름 | 좋음 | 저렴 | ✅ 기본 |
| GPT-4.1 Mini | 빠름 | 좋음 | 보통 | |
| GPT-5 Nano | 빠름 | 더 좋음 | 보통 | |
| GPT-5 Mini | 보통 | 더 좋음 | 높음 | |

### 3️⃣ 자연어 편집
```
"전체를 존댓말로 바꿔줘"
"전체를 더 전문적으로 만들어줘"
"전체에 이모지를 추가해줘"
"전체를 간결하게 줄여줘"
```

### 4️⃣ 다국어 지원
영어, 한국어, 일본어를 자동으로 감지하여 동일한 언어로 카드뉴스를 생성합니다.

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
- [x] Firebase Firestore 통합
- [x] 프로젝트 관리 시스템 (CRUD)
- [x] RSS 사이트 관리 UI
- [x] 크롤링 통계 및 로그
- [x] 100% 피드 보존 로직
- [x] 프로덕션 배포 (Render + Vercel)

**개발 기간**: 3일 (2025-10-25 ~ 2025-10-28)

### Phase 3 (Authentication, Notification & Design) - 🔜 예정
- [ ] 사용자 인증 (Firebase Authentication)
- [ ] 이메일 알림 시스템 (SendGrid)
- [ ] 웹 스크래핑 (Playwright)
- [ ] 디자인 템플릿 선택
- [ ] 이미지 생성 및 편집
- [ ] 카드뉴스 이미지 내보내기

## 📄 라이선스

MIT License

## 👤 작성자

Hyunil Lee

---

**Note**: 이 프로젝트는 Phase 2 (RSS Auto-Generation)까지 완료된 상태입니다. 

- **Phase 1**: 수동 카드뉴스 생성 (URL/텍스트 입력)
- **Phase 2**: RSS 자동 크롤링 및 카드뉴스 생성 ← 🆕 완료!
- **Phase 3**: 인증, 알림, 디자인 시스템 (예정)

상세한 개발 가이드는 [`docs/개발문서.md`](docs/개발문서.md)를, Phase 2 완료 보고서는 [`docs/PHASE2_COMPLETE.md`](docs/PHASE2_COMPLETE.md)를 참고하세요.
