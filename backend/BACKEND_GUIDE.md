# Backend 개발 가이드

## 📋 목차
1. [설치 및 실행](#설치-및-실행)
2. [프로젝트 구조](#프로젝트-구조)
3. [API 사용 예시](#api-사용-예시)
4. [환경 변수 설정](#환경-변수-설정)
5. [트러블슈팅](#트러블슈팅)

---

## 설치 및 실행

### 1. 가상환경 생성
```bash
cd backend
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 확인
`.env` 파일이 이미 생성되어 있습니다. 필요시 수정하세요.

### 4. 서버 실행
```bash
# 개발 모드 (자동 재시작)
uvicorn app.main:app --reload --port 8000

# 또는
python -m app.main
```

### 5. API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── config.py               # 환경 설정
│   │
│   ├── models/                 # Pydantic 모델
│   │   ├── project.py
│   │   ├── section.py
│   │   └── chat.py
│   │
│   ├── services/               # 비즈니스 로직
│   │   ├── scraper.py          # 웹 스크래핑
│   │   ├── summarizer.py       # AI 요약
│   │   ├── card_generator.py  # 카드 생성
│   │   └── chat_service.py     # AI 채팅
│   │
│   ├── routers/                # API 라우터
│   │   ├── projects.py
│   │   └── chat.py
│   │
│   └── utils/                  # 유틸리티
│       ├── firebase.py         # Firebase 연동
│       └── prompts.py          # AI 프롬프트
│
├── requirements.txt
└── .env                        # 환경 변수 (Git 제외)
```

---

## API 사용 예시

### 1. 프로젝트 생성 (URL 입력)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "url",
    "source_content": "https://example.com/article"
  }'
```

**Response:**
```json
{
  "id": "abc123-uuid",
  "source_type": "url",
  "source_content": "스크래핑된 제목 및 본문...",
  "summary": null,
  "keywords": null,
  "created_at": "2025-10-23T10:00:00Z",
  "updated_at": "2025-10-23T10:00:00Z",
  "status": "draft"
}
```

### 2. 프로젝트 생성 (텍스트 입력)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "source_content": "카드뉴스로 만들 내용입니다..."
  }'
```

### 3. 요약 생성

**Request:**
```bash
curl -X POST "http://localhost:8000/api/projects/{project_id}/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "max_length": 200
  }'
```

**Response:**
```json
{
  "summary": "핵심 요약 내용...",
  "keywords": ["키워드1", "키워드2", "키워드3"],
  "recommended_card_count": 5
}
```

### 4. 카드 섹션 생성

**Request:**
```bash
curl -X POST "http://localhost:8000/api/projects/{project_id}/sections"
```

**Response:**
```json
{
  "message": "섹션 생성 완료",
  "sections": [
    {
      "id": "section1",
      "order": 0,
      "type": "title",
      "title": "카드뉴스 제목",
      "content": "부제목",
      "design_config": {...}
    },
    ...
  ]
}
```

### 5. AI 채팅

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "abc123",
    "user_message": "두 번째 카드를 더 간결하게 만들어줘",
    "current_sections": [...],
    "conversation_history": []
  }'
```

**Response:**
```json
{
  "ai_response": "두 번째 카드의 내용을 간결하게 수정했습니다.",
  "updated_sections": [...],
  "action_taken": "modify"
}
```

---

## 환경 변수 설정

### `.env` 파일 구조

```env
# OpenAI API
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini

# Firebase
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_PATH=./serviceAccountKey.json

# Backend 설정
BACKEND_PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# 제한
MAX_TEXT_LENGTH=10000
RATE_LIMIT_PER_MINUTE=10

# Debug
DEBUG=True
LOG_LEVEL=INFO
```

### 중요 변수 설명

| 변수 | 설명 | 필수 여부 |
|------|------|-----------|
| `OPENAI_API_KEY` | OpenAI API 키 | ✅ 필수 |
| `OPENAI_MODEL` | 사용할 GPT 모델 | 선택 (기본: gpt-4o-mini) |
| `FIREBASE_PROJECT_ID` | Firebase 프로젝트 ID | Firebase 사용 시 필수 |
| `FIREBASE_PRIVATE_KEY_PATH` | 서비스 계정 키 파일 경로 | Firebase 사용 시 필수 |
| `ALLOWED_ORIGINS` | CORS 허용 오리진 (쉼표 구분) | 선택 |

---

## 트러블슈팅

### 1. `ModuleNotFoundError: No module named 'app'`

**해결 방법:**
```bash
# backend 디렉토리에서 실행하세요
cd backend
python -m app.main
```

### 2. OpenAI API 키 오류

**증상:**
```
openai.AuthenticationError: Incorrect API key provided
```

**해결 방법:**
1. `.env` 파일의 `OPENAI_API_KEY` 확인
2. API 키가 `sk-proj-`로 시작하는지 확인
3. OpenAI 대시보드에서 키 상태 확인

### 3. Firebase 연동 오류

**증상:**
```
Firebase initialization failed
```

**해결 방법:**
1. Firebase 프로젝트 생성 (Firebase Console)
2. 서비스 계정 키 다운로드 (`serviceAccountKey.json`)
3. `backend/` 디렉토리에 파일 배치
4. `.env`의 `FIREBASE_PROJECT_ID` 확인

**Firebase 없이 테스트하기:**
- Firebase 연동 없이도 스크래핑, 요약 기능은 작동합니다
- 프로젝트 저장 기능만 동작하지 않습니다

### 4. 웹 스크래핑 실패

**증상:**
```
ValueError: 웹 페이지를 스크래핑할 수 없습니다
```

**원인:**
- JavaScript로 렌더링되는 페이지
- 접근 제한이 있는 사이트
- 네트워크 오류

**해결 방법:**
- 일반 뉴스 사이트 URL로 테스트
- 또는 `source_type: "text"`로 직접 텍스트 입력

### 5. 포트 충돌

**증상:**
```
Error: Address already in use
```

**해결 방법:**
```bash
# 다른 포트로 실행
uvicorn app.main:app --reload --port 8001
```

---

## 테스트

### 헬스 체크
```bash
curl http://localhost:8000/health
```

**정상 응답:**
```json
{
  "status": "healthy",
  "openai_configured": true
}
```

### API 전체 플로우 테스트
```bash
# 1. 프로젝트 생성
PROJECT_ID=$(curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{"source_type":"text","source_content":"AI 기술이 빠르게 발전하고 있습니다..."}' \
  | jq -r '.id')

# 2. 요약 생성
curl -X POST "http://localhost:8000/api/projects/$PROJECT_ID/summarize"

# 3. 섹션 생성
curl -X POST "http://localhost:8000/api/projects/$PROJECT_ID/sections"

# 4. 섹션 조회
curl "http://localhost:8000/api/projects/$PROJECT_ID/sections"
```

---

## 로깅

로그는 콘솔에 출력됩니다. 레벨은 `.env`의 `LOG_LEVEL`로 조정할 수 있습니다.

```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

---

## 다음 단계
1. ✅ Backend 로컬 실행 테스트
2. ⏳ Firebase 프로젝트 설정 및 연동
3. ⏳ Frontend 개발 시작
4. ⏳ 통합 테스트

