# 🤖 AI 모델 업데이트 가이드 (GPT-4.1 / GPT-5)

## 📋 업데이트된 모델 목록

### 새로운 4개 모델 (2025년 최신)

| 모델 ID | 모델명 | 입력 가격 | 출력 가격 | 속도 | 품질 | 추천 |
|---------|--------|-----------|-----------|------|------|------|
| `gpt-4.1-nano` | GPT-4.1 Nano | $0.10/1M | $0.40/1M | 빠름 | 좋음 | ✅ 기본값 |
| `gpt-4.1-mini` | GPT-4.1 Mini | $0.15/1M | $0.60/1M | 빠름 | 좋음 | |
| `gpt-5-nano` | GPT-5 Nano | $0.20/1M | $0.80/1M | 빠름 | 더 좋음 | |
| `gpt-5-mini` | GPT-5 Mini | $0.25/1M | $2.00/1M | 보통 | 더 좋음 | |

---

## 🎯 모델 선택 가이드

### GPT-4.1 Nano (기본 추천) ⭐
- **최저 비용**: $0.10/1M 입력
- **빠른 속도**: 경량 작업에 최적
- **사용 사례**: 요약, 분류, 간단한 텍스트 생성
- **컨텍스트 윈도우**: 최대 100만 토큰

### GPT-4.1 Mini
- **균형잡힌 성능**: 속도와 품질의 균형
- **멀티모달**: 텍스트 및 비전 작업 지원
- **사용 사례**: 카드뉴스 생성, 이미지 분석
- **컨텍스트 윈도우**: 최대 100만 토큰

### GPT-5 Nano
- **향상된 성능**: GPT-4.1보다 개선된 정확도
- **리소스 효율적**: 제한된 환경에서도 우수한 성능
- **사용 사례**: 중요도 높은 요약, 정확한 키워드 추출
- **컨텍스트 윈도우**: 최대 40만 토큰

### GPT-5 Mini
- **최신 고성능**: 2025년 최신 기술
- **고품질 출력**: 가장 정확하고 자연스러운 텍스트
- **사용 사례**: 프리미엄 카드뉴스, 중요 문서 요약
- **컨텍스트 윈도우**: 최대 40만 토큰

---

## 💰 비용 비교 (1,000개 카드뉴스 생성 시)

### 예상 토큰 사용량 (카드뉴스 1개)
- 입력: 약 2,000 토큰 (원문 + 프롬프트)
- 출력: 약 500 토큰 (요약 + 카드 내용)

### 모델별 1,000개 생성 비용

| 모델 | 입력 비용 | 출력 비용 | 총 비용 |
|------|-----------|-----------|---------|
| GPT-4.1 Nano | $0.20 | $0.20 | **$0.40** |
| GPT-4.1 Mini | $0.30 | $0.30 | **$0.60** |
| GPT-5 Nano | $0.40 | $0.40 | **$0.80** |
| GPT-5 Mini | $0.50 | $1.00 | **$1.50** |

💡 **결론**: GPT-4.1 Nano를 기본값으로 사용하면 **가장 경제적**입니다!

---

## 🚀 Render 환경 변수 업데이트 (필수!)

### 1단계: Render Dashboard 접속
👉 https://dashboard.render.com/web/srv-d3t41ni4d50c73d28vn0

### 2단계: Environment 탭 클릭

### 3단계: OPENAI_MODEL 수정

#### 기존값 (오류 발생!)
```
gpt-4o-mini  ❌
```

#### 새로운 값 (선택)
```
gpt-4.1-nano  ✅ (추천)
gpt-4.1-mini
gpt-5-nano
gpt-5-mini
```

### 4단계: Save Changes 클릭

### 5단계: 재배포 대기 (2-3분)

---

## ✅ 업데이트 확인

### 1. 로컬에서 .env 파일 수정
```bash
cd backend
nano .env
```

**변경:**
```env
OPENAI_MODEL=gpt-4.1-nano
```

### 2. 로컬 백엔드 재시작
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

### 3. API 테스트
```bash
curl http://localhost:8000/api/status/openai
```

**정상 응답:**
```json
{
  "api_status": {
    "connected": true,
    "model": "gpt-4.1-nano",
    "status": "연결됨"
  }
}
```

---

## 🌐 프론트엔드 업데이트

**새로운 Vercel URL:**
🔗 https://frontend-n8aikk946-hyunils-projects.vercel.app

프론트엔드에서 4개의 모델 중 선택 가능:
- ✅ GPT-4.1 Nano (기본값, 가장 저렴)
- GPT-4.1 Mini
- GPT-5 Nano
- GPT-5 Mini

---

## 📊 주요 변경 사항

### 변경된 파일
1. `backend/app/config.py` - 기본 모델을 `gpt-4.1-nano`로 변경
2. `frontend/lib/constants/aiModels.ts` - 4개의 새로운 모델 추가
3. `frontend/components/source/SourceInput.tsx` - 기본 선택 모델 변경

### GitHub
- ✅ 코드 푸시 완료
- ✅ Render 자동 재배포 시작

### Vercel
- ✅ 프론트엔드 배포 완료
- 🌐 URL: https://frontend-n8aikk946-hyunils-projects.vercel.app

### Render
- ⏳ 재배포 진행 중
- ⚠️ 환경 변수 `OPENAI_MODEL=gpt-4.1-nano` 설정 필요!

---

## 🔧 문제 해결

### 문제 1: "Model gpt-4.1-nano not found"
**원인**: OpenAI API 키가 새로운 모델 접근 권한이 없음

**해결**:
1. OpenAI Dashboard 접속: https://platform.openai.com/account/limits
2. 모델 접근 권한 확인
3. 필요시 OpenAI 지원팀에 문의

---

### 문제 2: Render에서 여전히 이전 모델 사용
**원인**: 환경 변수가 업데이트되지 않음

**해결**:
1. Render Dashboard → Environment 탭
2. `OPENAI_MODEL` 값 확인/수정
3. Save Changes 클릭
4. Manual Deploy (필요시)

---

### 문제 3: API 호출 시 "max_tokens not supported" 에러
**원인**: GPT-5 시리즈는 `max_completion_tokens` 사용

**해결**: 코드에서 자동으로 처리됨 (향후 업데이트 예정)

---

## 📚 참고 자료

- [OpenAI Models Documentation](https://platform.openai.com/docs/models)
- [OpenAI Pricing](https://platform.openai.com/docs/pricing)
- [GPT-4.1 Release Notes](https://openai.com/index/gpt-4-1/)

---

## 📞 추가 지원

문제가 계속되면:
1. `RENDER_ENV_GUIDE.md` 참고
2. `RENDER_QUICK_FIX.md` 참고
3. Render Logs 탭에서 에러 확인

