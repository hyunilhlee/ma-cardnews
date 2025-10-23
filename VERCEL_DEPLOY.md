# 🚀 Vercel 배포 가이드

## 1단계: 프론트엔드 배포 (Vercel)

### 로그인
```bash
vercel login
```

### 프론트엔드 배포
```bash
cd /Users/hyunillee/Projects/CardNews/frontend
vercel
```

**설정 질문 답변:**
- Set up and deploy? → **Y (Yes)**
- Which scope? → **Your account**
- Link to existing project? → **N (No)**
- Project name? → **ma-cardnews** (또는 원하는 이름)
- In which directory is your code located? → **./** (엔터)
- Want to override settings? → **N (No)**

### 프로덕션 배포
```bash
vercel --prod
```

배포 완료 후 URL 받음: `https://ma-cardnews.vercel.app`

---

## 2단계: 백엔드 배포 (Render 추천)

### Render 사용 (무료 티어 있음)

1. https://render.com 접속 및 가입
2. **New → Web Service**
3. GitHub 저장소 연결
4. 설정:
   - **Name**: `ma-cardnews-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     OPENAI_API_KEY=sk-proj-...
     OPENAI_MODEL=gpt-4o-mini
     FIREBASE_PROJECT_ID=ma-cardnews
     ALLOWED_ORIGINS=https://ma-cardnews.vercel.app
     PORT=8000
     ```

5. **Create Web Service** 클릭

배포 완료 후 URL 받음: `https://ma-cardnews-api.onrender.com`

---

## 3단계: 환경 변수 연결

### Vercel 환경 변수 설정

```bash
cd frontend
vercel env add NEXT_PUBLIC_BACKEND_URL
```

**값 입력**: `https://ma-cardnews-api.onrender.com`

또는 Vercel 대시보드에서:
1. https://vercel.com/dashboard
2. 프로젝트 선택
3. **Settings → Environment Variables**
4. 추가:
   - **Key**: `NEXT_PUBLIC_BACKEND_URL`
   - **Value**: `https://ma-cardnews-api.onrender.com`
   - **Environment**: Production, Preview, Development (모두 체크)

### 재배포
```bash
vercel --prod
```

---

## 4단계: 커스텀 도메인 (선택사항)

### Vercel에서 도메인 추가
1. Vercel 대시보드
2. **Settings → Domains**
3. 도메인 입력 및 DNS 설정

---

## 완료! 🎉

### 접속 URL
- **프론트엔드**: https://ma-cardnews.vercel.app
- **백엔드**: https://ma-cardnews-api.onrender.com
- **API 문서**: https://ma-cardnews-api.onrender.com/docs

### 자동 배포
- GitHub에 push하면 자동으로 Vercel과 Render가 재배포합니다!

---

## 대안: 백엔드를 Railway로 배포

### Railway (더 빠름, 유료)
1. https://railway.app 접속
2. GitHub 연결
3. `backend` 폴더 선택
4. 환경 변수 설정
5. 자동 배포 ✅

---

## 트러블슈팅

### CORS 에러
→ 백엔드 `ALLOWED_ORIGINS`에 Vercel URL 추가

### 환경 변수 미적용
→ Vercel 재배포: `vercel --prod`

### 빌드 실패
→ `frontend` 폴더에서 `npm run build` 테스트

