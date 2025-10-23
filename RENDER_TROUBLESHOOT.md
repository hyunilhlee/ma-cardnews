# 🔧 Render 배포 실패 트러블슈팅

## 현재 상태
- ❌ Build failed: "Exited with status 1 while running your code"
- 이것은 **빌드는 성공**했지만 **코드 실행 중 실패**했다는 의미

## 🔍 로그 확인 방법

### 1. Render 대시보드 접속
https://dashboard.render.com/web/srv-d3t41ni4d50c73d28vn0

### 2. "Logs" 탭 클릭

### 3. 최신 로그에서 에러 찾기
다음과 같은 에러 패턴을 찾아주세요:

```
❌ ModuleNotFoundError: No module named 'XXX'
❌ KeyError: 'OPENAI_API_KEY'
❌ pydantic.errors.ValidationError
❌ Address already in use
❌ Application startup failed
```

## 🎯 가능한 문제와 해결책

### 문제 1: 환경 변수 누락
**증상**: `ValidationError: OPENAI_API_KEY`
**해결**: Environment 탭에서 환경 변수 확인

### 문제 2: 포트 바인딩 오류
**증상**: `Address already in use`
**해결**: Start Command 확인

### 문제 3: 모듈 Import 오류
**증상**: `ModuleNotFoundError`
**해결**: requirements.txt 확인

## ⚙️ Render 설정 체크리스트

### Build & Deploy 설정
- [ ] Root Directory = `backend`
- [ ] Build Command = `pip install -r requirements.txt`
- [ ] Start Command = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment Variables (필수!)
- [ ] `OPENAI_API_KEY` = sk-proj-...
- [ ] `OPENAI_MODEL` = gpt-4o-mini
- [ ] `FIREBASE_PROJECT_ID` = ma-cardnews
- [ ] `ALLOWED_ORIGINS` = https://frontend-pmrz3wvgk-hyunils-projects.vercel.app
- [ ] `DEBUG` = False
- [ ] `LOG_LEVEL` = INFO

## 📋 다음 단계

1. **Logs 탭에서 에러 메시지 복사**
2. **에러 메시지를 알려주세요**
3. 즉시 해결책 제공하겠습니다!

