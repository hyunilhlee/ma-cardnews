# Backend 서버 실행 가이드

## ✅ 완료된 작업
- Python 의존성 설치 완료
- pytest 버전 충돌 해결 (7.4.4로 다운그레이드)
- 모든 필요한 패키지 설치 완료

## 🚀 서버 실행 방법

터미널에서 다음 명령어를 실행하세요:

```bash
cd /Users/hyunillee/Projects/CardNews/backend
source venv/bin/activate  # 가상환경 활성화
python -m app.main
```

또는

```bash
cd /Users/hyunillee/Projects/CardNews/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

## 📋 서버 시작 확인

브라우저에서 다음 URL로 접속:
- API 문서: http://localhost:8000/docs
- 헬스 체크: http://localhost:8000/health
- 루트: http://localhost:8000/

## ⚠️ 주의사항

### Firebase 설정 선택사항
현재 Firebase 서비스 계정 키 파일이 없어도 **기본 기능은 작동합니다**:
- ✅ 웹 스크래핑
- ✅ AI 요약
- ✅ 카드 생성
- ❌ 프로젝트 저장 (Firebase 필요)

Firebase를 사용하려면:
1. Firebase Console에서 프로젝트 생성
2. 서비스 계정 키 다운로드
3. `backend/serviceAccountKey.json`에 저장

### OpenAI API 키
`.env` 파일에 API 키가 설정되어 있습니다.

## 🐛 트러블슈팅

에러가 발생하면:

1. **가상환경이 활성화되었는지 확인**
   ```bash
   which python  # /Users/hyunillee/Projects/CardNews/backend/venv/bin/python 이어야 함
   ```

2. **의존성 재설치**
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

3. **포트 충돌 확인**
   ```bash
   lsof -ti:8000 | xargs kill -9  # 8000번 포트 사용 중인 프로세스 종료
   ```

