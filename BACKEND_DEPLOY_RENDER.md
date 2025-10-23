# 🚀 백엔드 Render 배포 가이드

## 1단계: Render 계정 생성
1. https://render.com 접속
2. **Get Started** → GitHub로 가입

## 2단계: 새 Web Service 생성
1. 대시보드에서 **New +** → **Web Service**
2. GitHub 저장소 연결 (CardNews)
3. 저장소 선택 후 **Connect**

## 3단계: 서비스 설정

### Basic 설정
- **Name**: `ma-cardnews-api`
- **Region**: `Singapore` (또는 가까운 지역)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`

### Build & Deploy 설정
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

### Instance Type
- **Free** (무료 티어 선택)

## 4단계: 환경 변수 설정

**Environment Variables** 섹션에서 다음 변수들을 추가:

```env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
FIREBASE_PROJECT_ID=ma-cardnews
ALLOWED_ORIGINS=https://frontend-g69jlvvve-hyunils-projects.vercel.app
DEBUG=False
LOG_LEVEL=INFO
```

⚠️ **중요**: `ALLOWED_ORIGINS`에 Vercel URL을 정확히 입력!

## 5단계: 배포 시작
1. **Create Web Service** 클릭
2. 빌드 진행 (3-5분 소요)
3. 배포 완료 후 URL 확인: `https://ma-cardnews-api.onrender.com`

## 6단계: Vercel 환경 변수 업데이트

### 방법 1: CLI로 설정
```bash
cd frontend
vercel env add NEXT_PUBLIC_BACKEND_URL production
# 값 입력: https://ma-cardnews-api.onrender.com
vercel --prod
```

### 방법 2: 대시보드에서 설정
1. https://vercel.com/dashboard
2. 프로젝트 `frontend` 선택
3. **Settings** → **Environment Variables**
4. **Add New**:
   - **Name**: `NEXT_PUBLIC_BACKEND_URL`
   - **Value**: `https://ma-cardnews-api.onrender.com`
   - **Environments**: Production, Preview, Development 모두 체크
5. **Save**
6. **Deployments** → 최신 배포 → **Redeploy**

## ✅ 완료!

### 접속 테스트
- **프론트엔드**: https://frontend-g69jlvvve-hyunils-projects.vercel.app
- **백엔드 API**: https://ma-cardnews-api.onrender.com/docs
- **헬스 체크**: https://ma-cardnews-api.onrender.com/health

### 자동 배포 설정
- GitHub에 push → Vercel과 Render가 자동으로 재배포 ✅

## 🐛 트러블슈팅

### 문제: CORS 에러
**해결**: Render 환경 변수에서 `ALLOWED_ORIGINS` 확인

### 문제: OpenAI API 에러
**해결**: Render 환경 변수에서 `OPENAI_API_KEY` 확인

### 문제: 빌드 실패
**해결**: `backend/requirements.txt` 확인, Python 버전 확인

### 문제: Render 무료 티어 슬립 모드
**설명**: 무료 티어는 15분 비활성화 시 슬립 모드
**해결**: 첫 요청 시 1-2분 대기 (자동으로 깨어남)

