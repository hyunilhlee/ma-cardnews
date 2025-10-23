# CardNews AI Generator - 개발 체크리스트

## 📋 Phase 1 (MVP) 개발 체크리스트

### Week 1-2: 프로젝트 셋업 및 환경 구성

#### 1. 프로젝트 초기화
- [ ] GitHub 저장소 생성
- [ ] `.gitignore` 파일 작성 (Python, Node, Firebase 관련)
- [ ] README.md 기본 내용 작성
- [ ] 프로젝트 디렉토리 구조 생성 (backend, frontend)
- [ ] 라이선스 선택 및 추가

#### 2. Backend 환경 설정
- [ ] Python 가상환경 생성 (`python -m venv venv`)
- [ ] `requirements.txt` 작성
  - [ ] fastapi
  - [ ] uvicorn[standard]
  - [ ] pydantic
  - [ ] openai
  - [ ] beautifulsoup4
  - [ ] newspaper3k
  - [ ] requests
  - [ ] python-dotenv
  - [ ] firebase-admin
  - [ ] slowapi (rate limiting)
  - [ ] pytest (테스트)
  - [ ] pytest-cov (커버리지)
- [ ] 의존성 설치 (`pip install -r requirements.txt`)
- [ ] `.env.example` 파일 작성
- [ ] `.env` 파일 생성 (API 키 설정)
- [ ] FastAPI 기본 앱 생성 (`app/main.py`)
- [ ] 로컬 서버 실행 테스트 (`uvicorn app.main:app --reload`)

#### 3. Frontend 환경 설정
- [ ] Next.js 프로젝트 생성 (`npx create-next-app@latest frontend`)
- [ ] TypeScript 설정 확인
- [ ] Tailwind CSS 설치 및 설정
  - [ ] `npm install -D tailwindcss postcss autoprefixer`
  - [ ] `npx tailwindcss init -p`
  - [ ] `tailwind.config.js` 설정
- [ ] Zustand (상태 관리) 설치 (`npm install zustand`)
- [ ] Axios 설치 (`npm install axios`)
- [ ] `.env.local.example` 파일 작성
- [ ] `.env.local` 파일 생성
- [ ] 개발 서버 실행 테스트 (`npm run dev`)

#### 4. Firebase 설정
- [ ] Firebase 프로젝트 생성 (Firebase Console)
- [ ] Firebase CLI 설치 (`npm install -g firebase-tools`)
- [ ] Firebase 로그인 (`firebase login`)
- [ ] Firebase 프로젝트 초기화 (`firebase init`)
  - [ ] Hosting 선택
  - [ ] Firestore 선택
  - [ ] Storage 선택 (Phase 2용)
- [ ] Firestore 데이터베이스 생성 (테스트 모드)
- [ ] Firebase Admin SDK 서비스 계정 키 다운로드
  - [ ] Firebase Console > 프로젝트 설정 > 서비스 계정
  - [ ] `serviceAccountKey.json` 다운로드 후 backend/ 에 저장
  - [ ] `.gitignore`에 `serviceAccountKey.json` 추가
- [ ] Firestore 보안 규칙 작성 (`firestore.rules`)
- [ ] Frontend에 Firebase SDK 설치 (`npm install firebase`)
- [ ] Frontend Firebase 초기화 코드 작성

#### 5. 개발 도구 설정
- [ ] VS Code 확장 프로그램 설치
  - [ ] Python (Microsoft)
  - [ ] Pylance
  - [ ] ESLint
  - [ ] Tailwind CSS IntelliSense
  - [ ] Prettier
- [ ] Linter 설정 (Flake8, Black for Python)
- [ ] Prettier 설정 (Frontend)
- [ ] Pre-commit hooks 설정 (선택사항)

---

### Week 3-4: Backend API 개발

#### 6. Pydantic 모델 정의
- [ ] `models/project.py` 작성
  - [ ] ProjectCreate 모델
  - [ ] ProjectResponse 모델
  - [ ] SummarizeRequest 모델
  - [ ] SummarizeResponse 모델
- [ ] `models/section.py` 작성
  - [ ] CardSection 모델
  - [ ] SectionCreate 모델
  - [ ] SectionUpdate 모델
- [ ] `models/chat.py` 작성
  - [ ] ChatRequest 모델
  - [ ] ChatResponse 모델

#### 7. 웹 스크래핑 서비스 구현
- [ ] `services/scraper.py` 작성
  - [ ] WebScraper 클래스 생성
  - [ ] `scrape_url()` 메서드 (newspaper3k 사용)
  - [ ] `_fallback_scrape()` 메서드 (BeautifulSoup 사용)
  - [ ] 예외 처리 (타임아웃, 404 등)
- [ ] 테스트 작성 (`tests/test_scraper.py`)
  - [ ] 뉴스 기사 URL 테스트
  - [ ] 일반 블로그 URL 테스트
  - [ ] 잘못된 URL 처리 테스트

#### 8. AI 요약 서비스 구현
- [ ] `utils/prompts.py` 작성
  - [ ] SUMMARIZE_PROMPT 템플릿
  - [ ] KEYWORD_EXTRACTION_PROMPT 템플릿
- [ ] `services/summarizer.py` 작성
  - [ ] AISummarizer 클래스 생성
  - [ ] `summarize()` 메서드
  - [ ] `_generate_summary()` 메서드 (OpenAI API 호출)
  - [ ] `_extract_keywords()` 메서드
  - [ ] `_recommend_card_count()` 메서드
  - [ ] 토큰 사용량 최적화 (텍스트 truncate)
- [ ] 테스트 작성 (`tests/test_summarizer.py`)
  - [ ] 짧은 텍스트 요약 테스트
  - [ ] 긴 텍스트 요약 테스트
  - [ ] 키워드 추출 테스트

#### 9. 카드뉴스 생성 서비스 구현
- [ ] `utils/prompts.py`에 CARD_GENERATION_PROMPT 추가
- [ ] `services/card_generator.py` 작성
  - [ ] CardNewsGenerator 클래스 생성
  - [ ] `generate_sections()` 메서드
  - [ ] JSON 응답 파싱 로직
  - [ ] 카드 타입 검증 (title, content, closing)
- [ ] 테스트 작성 (`tests/test_card_generator.py`)

#### 10. AI 채팅 서비스 구현
- [ ] `utils/prompts.py`에 CHAT_SYSTEM_PROMPT 추가
- [ ] `services/chat_service.py` 작성
  - [ ] ChatService 클래스 생성
  - [ ] `process_chat_message()` 메서드
  - [ ] Function Calling 구현
    - [ ] modify_section 함수
    - [ ] reorder_sections 함수
  - [ ] `_format_sections_for_context()` 메서드
  - [ ] `_handle_function_call()` 메서드
- [ ] 테스트 작성 (`tests/test_chat_service.py`)

#### 11. Firebase 연동
- [ ] `utils/firebase.py` 작성
  - [ ] Firebase Admin SDK 초기화
  - [ ] Firestore 클라이언트 생성
  - [ ] 프로젝트 CRUD 함수
    - [ ] `create_project()`
    - [ ] `get_project()`
    - [ ] `update_project()`
  - [ ] 섹션 CRUD 함수
    - [ ] `create_sections()`
    - [ ] `get_sections()`
    - [ ] `update_section()`
  - [ ] 대화 이력 저장 함수
- [ ] 테스트 작성 (Firestore Emulator 사용)

#### 12. API 라우터 구현
- [ ] `routers/projects.py` 작성
  - [ ] POST /api/projects (프로젝트 생성)
  - [ ] GET /api/projects/{id} (프로젝트 조회)
  - [ ] POST /api/projects/{id}/summarize (요약)
  - [ ] POST /api/projects/{id}/sections (섹션 생성)
- [ ] `routers/sections.py` 작성
  - [ ] GET /api/sections (섹션 목록)
  - [ ] PATCH /api/sections/{id} (섹션 수정)
  - [ ] DELETE /api/sections/{id} (섹션 삭제)
- [ ] `routers/chat.py` 작성
  - [ ] POST /api/chat (AI 채팅)
- [ ] 통합 테스트 작성 (`tests/test_api.py`)
  - [ ] 전체 플로우 테스트 (생성 → 요약 → 섹션 생성 → 채팅)

#### 13. 에러 핸들링 및 검증
- [ ] `utils/validators.py` 작성
  - [ ] URL 유효성 검사
  - [ ] 텍스트 길이 검사
- [ ] 글로벌 예외 핸들러 추가 (`main.py`)
- [ ] HTTP 상태 코드 정리
  - [ ] 200: 성공
  - [ ] 201: 생성 성공
  - [ ] 400: 잘못된 요청
  - [ ] 404: 리소스 없음
  - [ ] 500: 서버 오류

#### 14. Rate Limiting 구현
- [ ] slowapi 설정
- [ ] API 엔드포인트별 제한 설정
  - [ ] POST /api/projects: 5/분
  - [ ] POST /api/chat: 10/분

---

### Week 5-6: Frontend UI 개발

#### 15. 공통 컴포넌트 개발
- [ ] `components/common/Button.tsx`
  - [ ] Primary, Secondary 버튼 스타일
  - [ ] 로딩 상태 표시
- [ ] `components/common/Input.tsx`
  - [ ] 텍스트 입력
  - [ ] URL 입력
  - [ ] 유효성 검사 표시
- [ ] `components/common/LoadingSpinner.tsx`
- [ ] `components/layout/Header.tsx`
  - [ ] 로고
  - [ ] 네비게이션 (Phase 2)
- [ ] `components/layout/Footer.tsx`

#### 16. 소스 입력 페이지 (Step 1)
- [ ] `pages/index.tsx` 작성
  - [ ] 랜딩 섹션 (서비스 설명)
  - [ ] 시작하기 버튼
- [ ] `components/source/SourceInput.tsx` 작성
  - [ ] URL/텍스트 탭 전환
  - [ ] 입력 폼
  - [ ] 제출 버튼
  - [ ] 로딩 상태
- [ ] `components/source/UrlValidator.tsx`
  - [ ] URL 유효성 실시간 검사
  - [ ] 에러 메시지 표시

#### 17. API 서비스 레이어
- [ ] `services/api.ts` (Axios 설정)
  - [ ] baseURL 설정
  - [ ] 인터셉터 (에러 핸들링)
- [ ] `services/projectService.ts`
  - [ ] createProject()
  - [ ] getProject()
  - [ ] summarizeProject()
  - [ ] generateSections()
- [ ] `services/chatService.ts`
  - [ ] sendChatMessage()

#### 18. 상태 관리 (Zustand)
- [ ] `store/projectStore.ts`
  - [ ] currentProject 상태
  - [ ] sections 상태
  - [ ] setProject, setSections 액션
- [ ] `store/uiStore.ts`
  - [ ] loading 상태
  - [ ] currentStep 상태

#### 19. 요약 표시 컴포넌트 (Step 2)
- [ ] `components/summary/SummaryView.tsx`
  - [ ] 요약문 표시
  - [ ] 추천 카드 수 표시
  - [ ] "카드뉴스 생성" 버튼
- [ ] `components/summary/KeywordBadges.tsx`
  - [ ] 키워드 뱃지 UI
  - [ ] 색상 및 애니메이션

#### 20. 카드뉴스 섹션 컴포넌트 (Step 3)
- [ ] `components/cardnews/CardList.tsx`
  - [ ] 섹션 목록 렌더링
  - [ ] 드래그 앤 드롭 순서 변경 (선택사항)
- [ ] `components/cardnews/CardPreview.tsx`
  - [ ] 개별 카드 미리보기
  - [ ] 타입별 스타일 (title, content, closing)
  - [ ] 간단한 디자인 (흰색 배경, 그림자)
- [ ] `components/cardnews/CardEditor.tsx` (선택사항)
  - [ ] 직접 편집 모드
  - [ ] 인라인 텍스트 수정

#### 21. AI 채팅 인터페이스
- [ ] `components/chat/ChatInterface.tsx`
  - [ ] 메시지 입력창
  - [ ] 전송 버튼
  - [ ] 대화 이력 표시
  - [ ] 로딩 상태 (AI가 생각 중)
- [ ] `components/chat/MessageBubble.tsx`
  - [ ] 사용자 메시지 (오른쪽)
  - [ ] AI 메시지 (왼쪽)
  - [ ] 타임스탬프

#### 22. 프로젝트 상세 페이지
- [ ] `pages/project/[id].tsx`
  - [ ] 프로젝트 로드
  - [ ] Step별 UI 전환
    - [ ] Step 1: 요약 대기
    - [ ] Step 2: 요약 결과 표시
    - [ ] Step 3: 카드 생성
    - [ ] Step 4: 편집 (카드 목록 + 채팅)
  - [ ] 에러 처리 (프로젝트 없음)

#### 23. 반응형 디자인
- [ ] 모바일 레이아웃 최적화 (Tailwind breakpoints)
  - [ ] `sm:` (640px)
  - [ ] `md:` (768px)
  - [ ] `lg:` (1024px)
- [ ] 태블릿 테스트
- [ ] 데스크탑 테스트

#### 24. TypeScript 타입 정의
- [ ] `types/project.ts`
  - [ ] Project 인터페이스
  - [ ] ProjectStatus enum
- [ ] `types/section.ts`
  - [ ] CardSection 인터페이스
  - [ ] CardType enum
- [ ] `types/chat.ts`
  - [ ] Message 인터페이스

---

### Week 7: AI 채팅 통합 및 실시간 기능

#### 25. 채팅 기능 통합
- [ ] 채팅 메시지 전송 시 API 호출
- [ ] AI 응답 수신 후 섹션 업데이트
- [ ] 대화 이력 로컬 상태 관리
- [ ] Firestore에 대화 이력 저장
- [ ] 재접속 시 대화 이력 복원

#### 26. 실시간 섹션 수정
- [ ] AI 응답으로 섹션 변경 시 UI 즉시 반영
- [ ] 낙관적 UI 업데이트 (Optimistic Update)
- [ ] 변경 애니메이션 추가
- [ ] Undo/Redo 기능 (선택사항)

#### 27. UX 개선
- [ ] 로딩 스피너 디자인 개선
- [ ] 에러 메시지 토스트 알림
- [ ] 성공 메시지 토스트 알림
- [ ] 빈 상태 UI (Empty State)
  - [ ] 프로젝트 없을 때
  - [ ] 섹션 없을 때
- [ ] 스켈레톤 로더 추가

#### 28. 접근성 (Accessibility)
- [ ] 키보드 네비게이션 지원
- [ ] ARIA 레이블 추가
- [ ] 색상 대비 확인 (WCAG AA 준수)
- [ ] 스크린 리더 테스트

---

### Week 8: 통합 테스트, 버그 수정, MVP 배포

#### 29. 통합 테스트
- [ ] E2E 테스트 작성 (Playwright 또는 Cypress)
  - [ ] 전체 플로우: 소스 입력 → 요약 → 카드 생성 → 채팅 수정
  - [ ] URL 입력 플로우
  - [ ] 텍스트 입력 플로우
- [ ] Backend 테스트 커버리지 확인 (80% 이상)
- [ ] API 통합 테스트 (실제 Firestore 연동)

#### 30. 버그 수정 및 최적화
- [ ] 버그 트래킹 시스템 설정 (GitHub Issues)
- [ ] 알려진 버그 수정
- [ ] 성능 프로파일링
  - [ ] API 응답 시간 측정
  - [ ] Frontend 렌더링 최적화
- [ ] 메모리 누수 확인

#### 31. 문서 작성
- [ ] README.md 업데이트
  - [ ] 프로젝트 설명
  - [ ] 설치 방법
  - [ ] 실행 방법
  - [ ] 환경 변수 설정
- [ ] API 문서 자동 생성 (FastAPI Swagger)
- [ ] 사용자 가이드 작성 (선택사항)

#### 32. 배포 준비
- [ ] 환경 변수 검토 및 정리
- [ ] Production 환경 `.env` 파일 준비
- [ ] Firebase 프로젝트 Production 모드 전환
- [ ] Firestore 보안 규칙 검토
- [ ] CORS 설정 확인

#### 33. Backend 배포 (Google Cloud Run)
- [ ] Dockerfile 작성 및 테스트
- [ ] Google Cloud 프로젝트 생성
- [ ] Cloud Build 설정
- [ ] 이미지 빌드 (`gcloud builds submit`)
- [ ] Cloud Run 배포
  - [ ] 리전 선택 (asia-northeast3)
  - [ ] 환경 변수 설정
  - [ ] 메모리 및 CPU 설정
- [ ] 배포 URL 확인 및 테스트
- [ ] 헬스 체크 확인 (`/health`)

#### 34. Frontend 배포 (Firebase Hosting)
- [ ] `.env.local`을 `.env.production`으로 복사
- [ ] `NEXT_PUBLIC_API_URL` 을 Cloud Run URL로 변경
- [ ] Production 빌드 (`npm run build`)
- [ ] Firebase 배포 (`firebase deploy --only hosting`)
- [ ] 배포된 사이트 테스트
- [ ] 커스텀 도메인 연결 (선택사항)

#### 35. 모니터링 및 로깅
- [ ] Google Cloud Logging 설정
- [ ] Firebase Analytics 설정 (선택사항)
- [ ] 에러 추적 도구 설정 (Sentry 등, 선택사항)
- [ ] API 사용량 모니터링 대시보드

#### 36. Phase 1 완료 체크
- [ ] 전체 기능 테스트
  - [ ] URL 입력 → 카드 생성 플로우
  - [ ] 텍스트 입력 → 카드 생성 플로우
  - [ ] AI 채팅으로 섹션 수정
- [ ] 성능 테스트
  - [ ] 페이지 로딩 속도 < 3초
  - [ ] API 응답 시간 < 5초
- [ ] 사용자 피드백 수집 (베타 테스터)
- [ ] Phase 1 회고 미팅

---

## 🚀 Phase 2 (Release) 개발 체크리스트

### Week 9-10: 자동 소스 탐색 및 크롤링

#### 37. 검색 API 연동
- [ ] Google Custom Search API 설정
- [ ] 또는 Bing Search API 설정
- [ ] `services/search_service.py` 작성
  - [ ] keyword_search() 메서드
  - [ ] 결과 필터링 (뉴스, 블로그만)
- [ ] API 라우터 추가 (`POST /api/search`)
- [ ] Frontend 검색 UI 추가

#### 38. 자동 크롤링 기능
- [ ] Selenium 또는 Playwright 설정 (JavaScript 렌더링 페이지용)
- [ ] 스케줄링 기능 (Cloud Scheduler + Cloud Functions)
- [ ] RSS 피드 파싱 기능
- [ ] 크롤링 결과 저장 (Firestore)

---

### Week 11-12: 다중 버전 제안 및 톤앤매너

#### 39. 다중 버전 생성
- [ ] `services/summarizer.py` 확장
  - [ ] `generate_multiple_versions()` 메서드
  - [ ] 3-5개 버전 생성 (다른 온도 값 사용)
- [ ] Frontend UI
  - [ ] 버전 선택 카드
  - [ ] 버전 비교 뷰

#### 40. 톤앤매너 선택
- [ ] 톤 옵션 정의 (전문적, 친근함, 유머러스, 공식적)
- [ ] 프롬프트 템플릿 확장
- [ ] Frontend 톤 선택 UI
- [ ] 선택된 톤으로 카드 재생성

---

### Week 13-14: 디자인 커스터마이징

#### 41. 템플릿 시스템
- [ ] 템플릿 모델 정의 (Firestore)
- [ ] 기본 템플릿 5-10개 제작
  - [ ] 미니멀
  - [ ] 비즈니스
  - [ ] 교육
  - [ ] 소셜 미디어
  - [ ] 뉴스
- [ ] 템플릿 선택 UI

#### 42. AI 디자인 수정
- [ ] `services/design_service.py` 작성
  - [ ] 자연어 디자인 명령 처리
  - [ ] "색상을 파란색으로" → hex 코드 변환
  - [ ] "폰트를 크게" → font_size 증가
- [ ] 디자인 채팅 인터페이스 (채팅 통합)

#### 43. 브랜드 커스터마이징
- [ ] 브랜드 색상 업로드
- [ ] 로고 업로드 (Firebase Storage)
- [ ] 폰트 선택 (Google Fonts 연동)
- [ ] 브랜드 프리셋 저장

---

### Week 15-16: 이미지 생성 및 Export

#### 44. 이미지 렌더링 엔진
- [ ] Pillow 또는 Playwright 사용
- [ ] HTML to Image 변환
  - [ ] `services/image_generator.py` 작성
  - [ ] HTML 템플릿 생성
  - [ ] 스크린샷 캡처
- [ ] 해상도 옵션
  - [ ] Instagram (1080x1080)
  - [ ] Instagram Story (1080x1920)
  - [ ] Facebook (1200x630)

#### 45. Export 기능
- [ ] API 엔드포인트 (`POST /api/projects/{id}/export`)
- [ ] PNG, JPG, PDF 형식 지원
- [ ] Firebase Storage 업로드
- [ ] 다운로드 URL 생성
- [ ] Frontend 다운로드 버튼
- [ ] ZIP 일괄 다운로드

#### 46. 최종 테스트 및 배포
- [ ] 전체 기능 통합 테스트
- [ ] 성능 테스트
- [ ] 사용자 수용 테스트 (UAT)
- [ ] Production 배포
- [ ] 공식 런칭 🎉

---

## 📊 테스트 체크리스트

### Backend 테스트
- [ ] 단위 테스트 (Services)
  - [ ] test_scraper.py
  - [ ] test_summarizer.py
  - [ ] test_card_generator.py
  - [ ] test_chat_service.py
- [ ] 통합 테스트 (API)
  - [ ] test_api.py
  - [ ] 전체 플로우 테스트
- [ ] 커버리지 80% 이상 달성

### Frontend 테스트
- [ ] 컴포넌트 단위 테스트 (Jest + React Testing Library)
- [ ] E2E 테스트 (Playwright)
  - [ ] 프로젝트 생성 플로우
  - [ ] 카드 수정 플로우
- [ ] 브라우저 호환성 테스트
  - [ ] Chrome
  - [ ] Safari
  - [ ] Firefox

---

## 🔒 보안 체크리스트
- [ ] API 키 환경 변수 관리
- [ ] `.env` 파일 `.gitignore`에 추가
- [ ] Firestore 보안 규칙 작성
- [ ] Rate Limiting 설정
- [ ] CORS 설정
- [ ] 입력 검증 (XSS, SQL Injection 방지)
- [ ] HTTPS 강제 (Production)

---

## 📈 성능 최적화 체크리스트
- [ ] API 응답 캐싱 (Redis, 선택사항)
- [ ] 이미지 최적화 (WebP 포맷)
- [ ] Code Splitting (Next.js 자동)
- [ ] Lazy Loading
- [ ] CDN 활용 (Firebase Hosting 자동)
- [ ] Database 인덱스 최적화

---

## 📝 문서 체크리스트
- [ ] README.md 작성
- [ ] API 문서 (Swagger)
- [ ] 개발 가이드 (이 문서)
- [ ] 배포 가이드
- [ ] 사용자 매뉴얼
- [ ] 라이선스 파일
- [ ] CHANGELOG.md

---

## 🎯 마일스톤

| 마일스톤 | 목표일 | 상태 |
|---------|--------|------|
| **M1: 프로젝트 셋업 완료** | Week 2 종료 | ⬜ |
| **M2: Backend API 완성** | Week 4 종료 | ⬜ |
| **M3: Frontend UI 완성** | Week 6 종료 | ⬜ |
| **M4: Phase 1 MVP 배포** | Week 8 종료 | ⬜ |
| **M5: Phase 2 기능 개발 완료** | Week 14 종료 | ⬜ |
| **M6: Phase 2 정식 런칭** | Week 16 종료 | ⬜ |

---

## 💡 추가 개선 아이디어 (Backlog)
- [ ] 사용자 인증 및 계정 관리 (Firebase Auth)
- [ ] 프로젝트 히스토리 (버전 관리)
- [ ] 협업 기능 (여러 사용자가 함께 편집)
- [ ] AI 이미지 생성 (DALL-E, Stable Diffusion)
- [ ] 다국어 지원
- [ ] 분석 대시보드 (조회수, 공유 수 등)
- [ ] SNS 자동 포스팅 연동
- [ ] 프리미엄 템플릿 마켓플레이스

---

**체크리스트 버전**: 1.0  
**최종 업데이트**: 2025-10-23  
**작성자**: CardNews AI Development Team

**사용 방법**:
1. 각 항목을 완료하면 `[ ]`를 `[x]`로 변경하세요.
2. 새로운 작업이 발견되면 해당 섹션에 추가하세요.
3. 주간 단위로 진행 상황을 리뷰하세요.

