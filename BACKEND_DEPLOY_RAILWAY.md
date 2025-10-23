# 🚀 백엔드 Railway 배포 가이드 (더 빠름)

## Railway가 Render보다 좋은 이유
✅ 슬립 모드 없음 (항상 온라인)
✅ 더 빠른 응답 속도
✅ GitHub 자동 배포
⚠️ 무료 크레딧 $5/월 (이후 유료)

## 1단계: Railway 계정 생성
1. https://railway.app 접속
2. **Start a New Project** → GitHub로 가입

## 2단계: 프로젝트 배포
1. **New Project** → **Deploy from GitHub repo**
2. 저장소 선택: `CardNews`
3. **Deploy Now** 클릭

## 3단계: 서비스 설정
1. 배포된 서비스 클릭
2. **Settings** 탭

### Root Directory 설정
- **Root Directory**: `backend`

### Start Command 설정
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Build Command (선택사항)
- **Build Command**: `pip install -r requirements.txt`

## 4단계: 환경 변수 설정
1. **Variables** 탭
2. **New Variable** 클릭
3. 다음 변수들 추가:

```env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
FIREBASE_PROJECT_ID=ma-cardnews
ALLOWED_ORIGINS=https://frontend-g69jlvvve-hyunils-projects.vercel.app
DEBUG=False
LOG_LEVEL=INFO
PORT=8000
```

## 5단계: Public URL 생성
1. **Settings** 탭
2. **Networking** 섹션
3. **Generate Domain** 클릭
4. URL 확인: `https://your-project.up.railway.app`

## 6단계: Vercel 환경 변수 업데이트

```bash
cd frontend
vercel env add NEXT_PUBLIC_BACKEND_URL production
# 값 입력: https://your-project.up.railway.app
vercel --prod
```

또는 Vercel 대시보드에서 직접 설정

## ✅ 완료!

### 접속 테스트
- **프론트엔드**: https://frontend-g69jlvvve-hyunils-projects.vercel.app
- **백엔드 API**: https://your-project.up.railway.app/docs
- **헬스 체크**: https://your-project.up.railway.app/health

### 비용
- **무료 크레딧**: $5/월
- **이후**: 사용량 기반 ($0.000463/GB-시간)
- **예상 비용**: $5-10/월 (낮은 트래픽)

## 🎯 Railway vs Render 비교

| 특징 | Railway | Render |
|------|---------|--------|
| 무료 티어 | $5 크레딧/월 | 무제한 (슬립 모드) |
| 슬립 모드 | ❌ 없음 | ✅ 있음 (15분) |
| 속도 | ⚡ 빠름 | 🐢 느림 |
| 자동 배포 | ✅ | ✅ |
| 설정 난이도 | 😊 쉬움 | 😊 쉬움 |

## 추천
- **개발/테스트**: Render (무료)
- **프로덕션**: Railway (빠르고 안정적)

