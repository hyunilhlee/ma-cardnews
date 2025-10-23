# 🚀 배포 가이드

## Firebase 프로젝트 설정

### 1. Firebase 프로젝트 생성
```bash
# Firebase 콘솔에서 프로젝트 생성
# https://console.firebase.google.com/
# 프로젝트 ID: ma-cardnews
```

### 2. 옵션 A: Firebase Hosting + Cloud Run (권장)

#### 프론트엔드 배포 (Cloud Run)
```bash
# 프론트엔드 빌드 및 배포
cd frontend
gcloud builds submit --tag gcr.io/ma-cardnews/frontend
gcloud run deploy cardnews-frontend \
  --image gcr.io/ma-cardnews/frontend \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_BACKEND_URL=https://cardnews-api-<hash>-an.a.run.app
```

#### 백엔드 배포 (Cloud Run)
```bash
# 백엔드 빌드 및 배포
cd backend
gcloud builds submit --tag gcr.io/ma-cardnews/backend
gcloud run deploy cardnews-api \
  --image gcr.io/ma-cardnews/backend \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-api-key
```

### 3. 옵션 B: Firebase Hosting (정적 사이트만 가능)

**주의**: Next.js 동적 라우팅이 필요하므로 권장하지 않음

```bash
# 정적 페이지만 배포 (제한적)
cd frontend
npm run build
firebase deploy --only hosting
```

## 환경 변수 설정

### 프론트엔드 (.env.production)
```env
NEXT_PUBLIC_BACKEND_URL=https://cardnews-api-<hash>-an.a.run.app
```

### 백엔드 (.env)
```env
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
FIREBASE_PROJECT_ID=ma-cardnews
ALLOWED_ORIGINS=https://cardnews-frontend-<hash>-an.a.run.app
```

## 배포 명령어

### Cloud Run 배포 (권장)
```bash
# 1. 프론트엔드
cd frontend
gcloud builds submit --tag gcr.io/ma-cardnews/frontend
gcloud run deploy cardnews-frontend --image gcr.io/ma-cardnews/frontend --platform managed --region asia-northeast3

# 2. 백엔드
cd ../backend
gcloud builds submit --tag gcr.io/ma-cardnews/backend
gcloud run deploy cardnews-api --image gcr.io/ma-cardnews/backend --platform managed --region asia-northeast3
```

### Firebase Hosting (제한적)
```bash
# 홈페이지만 정적 배포
firebase deploy --only hosting
```

## 도메인 연결

### Firebase Hosting
```bash
firebase hosting:channel:deploy live
```

### Cloud Run 커스텀 도메인
```bash
gcloud run domain-mappings create --service cardnews-frontend --domain www.your-domain.com
```

## 비용 최적화

### Cloud Run 설정
- **최소 인스턴스**: 0 (비용 절감)
- **최대 인스턴스**: 10
- **메모리**: 512MB
- **CPU**: 1

### Firebase Hosting
- **무료 티어**: 10GB/월
- **대역폭**: 360MB/일

## 모니터링

### Cloud Run 로그
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

### Firebase Hosting
```bash
firebase hosting:channel:list
```

## 트러블슈팅

### 문제: 동적 라우팅이 작동하지 않음
**해결**: Cloud Run 사용 (Firebase Hosting은 정적 사이트만 지원)

### 문제: CORS 에러
**해결**: 백엔드 `ALLOWED_ORIGINS`에 프론트엔드 URL 추가

### 문제: 환경 변수 미적용
**해결**: Cloud Run 서비스 설정에서 환경 변수 확인

## 추천 배포 방식

**Production**: Cloud Run (프론트엔드 + 백엔드)
- 완전한 Next.js 기능 지원
- 동적 라우팅 지원
- 서버 사이드 렌더링
- API 통합

**Staging**: Firebase Hosting Preview Channels
- 빠른 프리뷰
- PR별 미리보기
- 정적 페이지 테스트

