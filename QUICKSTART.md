# 🚀 빠른 시작 가이드

CardNews AI Generator를 5분 안에 실행하는 방법

## ⚡ 한 번에 실행하기

### 1. Backend 실행

```bash
# 터미널 창 #1
cd backend
source venv/bin/activate  # 이미 가상환경이 생성되어 있음
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend 실행

```bash
# 터미널 창 #2
cd frontend
npm run dev
```

### 3. 브라우저 열기

- **Frontend**: http://localhost:3000
- **Backend API 문서**: http://localhost:8000/docs

## ✅ 빠른 테스트

### 1. 홈페이지에서 테스트

1. http://localhost:3000 접속
2. "텍스트 직접 입력" 선택
3. 아래 예시 텍스트 복사 & 붙여넣기

```
인공지능 기술이 빠르게 발전하고 있습니다. 많은 기업들이 AI를 활용하여 업무 효율성을 높이고 있으며, 특히 생성형 AI는 콘텐츠 제작 분야에서 혁신을 이루고 있습니다. ChatGPT와 같은 대화형 AI는 이미 수백만 명의 사용자를 확보했습니다. 앞으로 AI 기술은 더욱 발전하여 우리 생활의 많은 부분을 변화시킬 것으로 예상됩니다.
```

4. "카드뉴스 만들기" 클릭
5. AI가 요약하면 "카드뉴스 생성하기" 클릭
6. 생성된 카드 확인 후 AI 채팅으로 수정 테스트!

### 2. API로 직접 테스트

http://localhost:8000/docs 에서 Swagger UI를 통해 직접 API를 테스트할 수 있습니다.

## 🔍 문제 해결

### Backend 서버가 안 켜져요

```bash
# 가상환경이 활성화되어 있는지 확인
which python  # /Users/.../CardNews/backend/venv/bin/python 이어야 함

# .env 파일이 있는지 확인
cat backend/.env

# 의존성 재설치
pip install -r requirements.txt
```

### Frontend 서버가 안 켜져요

```bash
# node_modules 재설치
rm -rf node_modules package-lock.json
npm install

# .env.local 파일 확인
cat frontend/.env.local
```

### API 호출이 실패해요

1. Backend 서버가 http://localhost:8000에서 실행 중인지 확인
2. 브라우저 콘솔(F12)에서 CORS 에러 확인
3. Backend 로그에서 에러 메시지 확인

## 💡 유용한 명령어

### Backend

```bash
# 로그 확인하며 실행
cd backend && source venv/bin/activate && uvicorn app.main:app --reload --log-level debug

# 테스트 실행
cd backend && source venv/bin/activate && pytest

# 포트가 사용 중일 때
lsof -ti:8000 | xargs kill -9
```

### Frontend

```bash
# 빌드 테스트
npm run build

# 타입 체크
npx tsc --noEmit

# 포트가 사용 중일 때
lsof -ti:3000 | xargs kill -9
```

## 📚 다음 단계

- [README.md](./README.md) - 전체 프로젝트 문서
- [개발문서.md](./개발문서.md) - 상세한 개발 가이드
- [TODO.md](./TODO.md) - 개발 진행 상황

---

**즐거운 개발 되세요! 🎉**

