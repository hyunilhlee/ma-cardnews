# 🚀 Render 환경 변수 설정 가이드

## 📋 환경 변수 요약

### ✅ 필수 (1개)
| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `sk-proj-YOUR_OPENAI_API_KEY_HERE` |

### 🎨 권장 (4개)
| Key | Value | 설명 |
|-----|-------|------|
| `OPENAI_MODEL` | `gpt-4o-mini` | ⚠️ 설정 안 하면 `gpt-5-nano` 에러 발생! |
| `FIREBASE_PROJECT_ID` | `ma-cardnews` | Firebase 프로젝트 ID |
| `DEBUG` | `False` | 프로덕션 모드 |
| `LOG_LEVEL` | `INFO` | 로그 수준 |

### ⚙️ 선택 (2개) - 기본값 있음
| Key | Default | 설명 |
|-----|---------|------|
| `MAX_TEXT_LENGTH` | `10000` | 입력 텍스트 최대 길이 |
| `RATE_LIMIT_PER_MINUTE` | `10` | API 요청 제한 (분당) |

---

## 🔗 Render 대시보드 링크

**Backend Service:**
👉 https://dashboard.render.com/web/srv-d3t41ni4d50c73d28vn0

**Environment 탭에서 설정**

---

## 📝 설정 방법

### 1. Render Dashboard 접속
위 링크 클릭

### 2. Environment 탭 클릭

### 3. 기존 불필요 변수 삭제
- ❌ `ALLOWED_ORIGINS` (더 이상 사용 안 함)
- ❌ `FIREBASE_PRIVATE_KEY_PATH` (Render에서 불필요)

### 4. 새 환경 변수 추가
"Add Environment Variable" 버튼 클릭 후 아래 값들 입력

#### OPENAI_API_KEY (필수!)
```
sk-proj-YOUR_OPENAI_API_KEY_HERE
```
⚠️ **앞뒤 공백 없이 정확히 복사!**
⚠️ **실제 API 키는 .env 파일이나 Render 환경 변수에만 저장하세요!**

#### OPENAI_MODEL (권장!)
```
gpt-4o-mini
```

#### FIREBASE_PROJECT_ID (권장)
```
ma-cardnews
```

#### DEBUG (권장)
```
False
```

#### LOG_LEVEL (권장)
```
INFO
```

#### MAX_TEXT_LENGTH (선택)
```
10000
```

#### RATE_LIMIT_PER_MINUTE (선택)
```
10
```

### 5. Save Changes 클릭

### 6. 자동 재배포 대기
- Events 탭에서 "Deploy started" 확인
- Logs 탭에서 빌드 진행 상황 확인
- 2-3분 후 상태가 "Live"로 변경

---

## ✅ 배포 후 테스트

### 방법 1: 터미널에서 테스트
```bash
./test-render-api.sh
```

### 방법 2: 수동 테스트
```bash
# 헬스 체크
curl https://ma-cardnews-api.onrender.com/health

# OpenAI 상태 체크
curl https://ma-cardnews-api.onrender.com/api/status/openai
```

### 예상 응답 (정상)
```json
{
  "status": "connected",
  "model": "gpt-4o-mini",
  "message": "OpenAI API에 성공적으로 연결되었습니다."
}
```

### 예상 응답 (에러)
```json
{
  "status": "error",
  "model": "gpt-4o-mini",
  "message": "OpenAI API 키가 유효하지 않습니다."
}
```

---

## 🔍 문제 해결

### 문제 1: "401 Unauthorized"
**원인:** `OPENAI_API_KEY`가 누락되었거나 잘못됨

**해결:**
1. Environment 탭에서 `OPENAI_API_KEY` 확인
2. 값이 정확한지 확인 (앞뒤 공백 없이!)
3. Save 후 재배포

---

### 문제 2: "Model gpt-5-nano not found"
**원인:** `OPENAI_MODEL`이 설정되지 않아 기본값 사용

**해결:**
1. Environment 탭에서 `OPENAI_MODEL` 추가
2. 값: `gpt-4o-mini`
3. Save 후 재배포

---

### 문제 3: CORS 에러
**원인:** 코드는 수정했지만 재배포 안 됨

**해결:**
1. Manual Deploy 클릭
2. 또는 GitHub에 더미 커밋 후 push

---

## 📊 환경 변수 우선순위

1. **Render Environment Variables** (최우선)
2. `backend/.env` 파일 (로컬 개발용)
3. `backend/app/config.py` 기본값

⚠️ **중요:** Render에서는 `.env` 파일이 업로드되지 않으므로, 반드시 Environment Variables에 설정해야 합니다!

---

## 🔐 보안 주의사항

- ✅ API 키는 절대 GitHub에 커밋하지 마세요
- ✅ Render Environment Variables는 자동으로 암호화됩니다
- ✅ `.gitignore`에 `.env` 파일이 포함되어 있는지 확인
- ✅ API 키는 주기적으로 교체하는 것이 좋습니다

---

## 📞 추가 도움

문제가 계속되면:
1. Render Logs 탭에서 에러 로그 확인
2. `test-render-api.sh` 스크립트 실행 결과 공유
3. Environment 탭 스크린샷 공유 (API 키는 가림)

