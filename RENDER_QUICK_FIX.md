# 🚨 Render 긴급 수정 가이드

## 문제
- OpenAI API 연결 실패
- `gpt-5-nano` 모델 에러 (존재하지 않는 모델)

## 해결 방법

### 1. Render 대시보드 접속
👉 https://dashboard.render.com/web/srv-d3t41ni4d50c73d28vn0

### 2. Environment 탭 클릭

### 3. 환경 변수 추가

#### OPENAI_API_KEY
- Key: `OPENAI_API_KEY`
- Value: `여러분의_실제_OpenAI_API_키`
- ⚠️ `sk-proj-`로 시작하는 키

#### OPENAI_MODEL (중요!)
- Key: `OPENAI_MODEL`
- Value: `gpt-4o-mini`

#### 선택사항
- Key: `FIREBASE_PROJECT_ID`, Value: `ma-cardnews`
- Key: `DEBUG`, Value: `False`
- Key: `LOG_LEVEL`, Value: `INFO`

### 4. Save Changes

### 5. 재배포 대기 (2-3분)

## 확인 방법

```bash
# 헬스 체크
curl https://ma-cardnews-api.onrender.com/health

# OpenAI 상태 확인
curl https://ma-cardnews-api.onrender.com/api/status/openai
```

**성공 응답:**
```json
{
  "api_status": {
    "connected": true,
    "model": "gpt-4o-mini",
    "status": "연결됨",
    "message": "OpenAI API에 성공적으로 연결되었습니다."
  }
}
```

## 주의사항

1. **OPENAI_API_KEY**: 반드시 실제 API 키 입력 (앞뒤 공백 없이!)
2. **OPENAI_MODEL**: `gpt-4o-mini` 정확히 입력
3. **Save 후 재배포**: 반드시 재배포가 완료될 때까지 대기

## 문제가 계속되면?

1. Render Logs 탭에서 에러 확인
2. Environment 탭에서 변수 이름 오타 확인
3. API 키 유효성 확인: https://platform.openai.com/api-keys

