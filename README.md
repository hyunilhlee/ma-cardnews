# 📰 CardNews AI Generator

AI 기반 카드뉴스 자동 생성 서비스 - Phase 1 (MVP)

## 🎯 프로젝트 개요

링크 또는 텍스트를 입력하면 AI가 자동으로 카드뉴스를 생성하고, 자연어로 대화하며 내용을 수정할 수 있는 웹 서비스입니다.

### 주요 기능

- ✅ **다양한 소스 입력**: URL 링크 또는 텍스트 직접 입력
- ✅ **AI 자동 요약**: GPT-4o-mini를 활용한 핵심 내용 추출 및 키워드 분석
- ✅ **자동 카드 생성**: 적절한 구조와 디자인으로 카드뉴스 자동 생성
- ✅ **자연어 편집**: AI와 대화하며 내용을 쉽게 수정하고 개선

## 🛠️ 기술 스택

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Notifications**: react-hot-toast

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **AI**: OpenAI GPT-4o-mini
- **Web Scraping**: newspaper3k, BeautifulSoup4
- **Validation**: Pydantic
- **Database**: Firebase Firestore (선택사항)

## 📂 프로젝트 구조

```
CardNews/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── config.py          # 환경 설정
│   │   ├── main.py            # FastAPI 앱
│   │   ├── models/            # Pydantic 모델
│   │   ├── services/          # 비즈니스 로직
│   │   ├── routers/           # API 라우터
│   │   └── utils/             # 유틸리티
│   ├── requirements.txt       # Python 의존성
│   └── .env                   # 환경 변수
│
├── frontend/                  # Next.js 프론트엔드
│   ├── app/                   # Next.js 페이지
│   ├── components/            # React 컴포넌트
│   │   ├── common/           # 공통 컴포넌트
│   │   ├── source/           # 소스 입력
│   │   ├── summary/          # 요약 표시
│   │   ├── cardnews/         # 카드뉴스
│   │   ├── chat/             # AI 채팅
│   │   └── layout/           # 레이아웃
│   ├── lib/                  # 라이브러리
│   │   ├── types/            # TypeScript 타입
│   │   ├── services/         # API 서비스
│   │   └── store/            # Zustand 스토어
│   └── .env.local            # 환경 변수
│
├── PRD.md                    # 제품 요구사항 문서
├── 개발문서.md                # 개발 가이드
└── TODO.md                   # 개발 체크리스트
```

## 🚀 시작하기

### 1. Backend 설정 및 실행

```bash
# 백엔드 디렉토리로 이동
cd backend

# Python 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일 생성)
# OPENAI_API_KEY, FIREBASE_PROJECT_ID 등 설정 필요

# 서버 실행
python -m uvicorn app.main:app --reload --port 8000
```

**Backend API**: http://localhost:8000  
**API 문서**: http://localhost:8000/docs

### 2. Frontend 설정 및 실행

```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정 (.env.local 파일)
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 개발 서버 실행
npm run dev
```

**Frontend**: http://localhost:3000

## 📖 사용 방법

### Step 1: 소스 입력
1. 홈페이지 접속 (http://localhost:3000)
2. URL 링크 또는 텍스트 입력
3. "카드뉴스 만들기" 버튼 클릭

### Step 2: 요약 확인
1. AI가 자동으로 생성한 요약 확인
2. 핵심 키워드 및 권장 카드 수 확인
3. "카드뉴스 생성하기" 버튼 클릭

### Step 3: 편집 및 완성
1. 자동 생성된 카드뉴스 확인
2. AI 채팅으로 내용 수정
   - 예: "첫 번째 카드의 제목을 더 강렬하게 바꿔줘"
   - 예: "두 번째와 세 번째 카드의 순서를 바꿔줘"
3. 실시간으로 반영되는 카드 확인

## 🔧 환경 변수 설정

### Backend (.env)
```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Firebase (선택사항)
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY_PATH=./serviceAccountKey.json

# Backend 설정
BACKEND_PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
MAX_TEXT_LENGTH=10000
RATE_LIMIT_PER_MINUTE=10
DEBUG=True
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| **POST** | `/api/projects` | 프로젝트 생성 |
| **GET** | `/api/projects/{id}` | 프로젝트 조회 |
| **POST** | `/api/projects/{id}/summarize` | 요약 생성 |
| **POST** | `/api/projects/{id}/sections` | 카드 섹션 생성 |
| **GET** | `/api/projects/{id}/sections` | 섹션 목록 조회 |
| **POST** | `/api/chat` | AI 채팅 메시지 전송 |

자세한 API 문서는 http://localhost:8000/docs 참고

## 🧪 테스트

### Backend 테스트
```bash
cd backend
pytest --cov=app tests/
```

### Frontend 빌드
```bash
cd frontend
npm run build
```

## 🔒 보안 주의사항

- ⚠️ **OpenAI API 키**는 절대 Git에 커밋하지 마세요
- `.env` 파일은 `.gitignore`에 포함되어 있습니다
- 프로덕션 환경에서는 반드시 환경 변수를 안전하게 관리하세요

## 📝 개발 진행 상황

현재 **Phase 1 (MVP)** 개발이 완료되었습니다.

✅ **완료된 작업**
- Backend API 구현 (FastAPI)
- Frontend UI 구현 (Next.js)
- AI 요약 및 카드 생성 기능
- AI 채팅 기반 편집 기능
- 반응형 디자인

⏳ **예정된 작업** (Phase 2)
- 자동 소스 크롤링
- 다양한 요약 버전 제안
- 디자인 커스터마이징
- 이미지 Export 기능
- Firebase 배포

자세한 내용은 [TODO.md](./TODO.md) 참고

## 👥 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

## 📄 라이선스

MIT License

## 📞 문의

문제가 발생하거나 질문이 있으시면 이슈를 등록해주세요.

---

**Made with ❤️ and AI**
