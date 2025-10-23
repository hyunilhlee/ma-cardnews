# 🚀 빠른 배포 가이드

## Firebase 프로젝트는 정적 호스팅만 가능합니다

Next.js의 동적 라우팅(`/project/[id]`)을 사용하고 있어서,
Firebase Hosting만으로는 완전한 배포가 불가능합니다.

## 추천 배포 방법

### ✅ 옵션 1: Vercel (가장 간단 - 무료)

```bash
# Vercel CLI 설치
npm i -g vercel

# 프론트엔드 배포
cd frontend
vercel

# 백엔드는 Google Cloud Run 또는 Railway 사용
```

### ✅ 옵션 2: Google Cloud Run (완전한 배포)

```bash
# Google Cloud 프로젝트 설정
gcloud config set project ma-cardnews

# 프론트엔드 배포
cd frontend
gcloud builds submit --tag gcr.io/ma-cardnews/frontend
gcloud run deploy cardnews-frontend \
  --image gcr.io/ma-cardnews/frontend \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated

# 백엔드 배포
cd ../backend  
gcloud builds submit --tag gcr.io/ma-cardnews/backend
gcloud run deploy cardnews-api \
  --image gcr.io/ma-cardnews/backend \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated
```

### ✅ 옵션 3: Railway (간편 - 유료)

1. https://railway.app 접속
2. GitHub 연결
3. 프로젝트 선택
4. 자동 배포

## Firebase는 어디에 사용하나요?

- **Firestore**: 데이터베이스 (이미 코드에 구현됨)
- **Firebase Auth**: 사용자 인증 (Phase 2)
- **Firebase Storage**: 이미지 저장 (Phase 2)

## 현재 상황

- ❌ Firebase Hosting: 동적 라우팅 미지원
- ✅ Vercel: Next.js에 최적화, 무료
- ✅ Cloud Run: 완전한 컨트롤, Firebase 통합 쉬움
- ✅ Railway: 가장 간편, 자동 배포

## 추천

**개발/테스트**: Vercel (프론트엔드) + 로컬 (백엔드)
**프로덕션**: Cloud Run (둘 다)
