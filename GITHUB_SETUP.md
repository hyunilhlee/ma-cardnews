# 📦 GitHub 저장소 생성 및 Push

## 1단계: GitHub에서 새 저장소 생성

1. https://github.com/new 접속
2. 저장소 설정:
   - **Repository name**: `CardNews` (또는 원하는 이름)
   - **Description**: AI 기반 카드뉴스 생성기
   - **Public** 또는 **Private** 선택
   - ❌ **"Initialize this repository with" 모두 체크 해제**
3. **Create repository** 클릭

## 2단계: 로컬 저장소를 GitHub에 연결

GitHub에서 제공하는 URL을 복사 (예: `https://github.com/username/CardNews.git`)

터미널에서 실행:

```bash
cd /Users/hyunillee/Projects/CardNews

# GitHub 저장소 연결
git remote add origin https://github.com/username/CardNews.git

# 메인 브랜치로 이름 변경 (필요시)
git branch -M main

# GitHub에 Push
git push -u origin main
```

## 3단계: Render에서 저장소 연결

1. **Render 대시보드**: https://dashboard.render.com
2. **New + → Web Service**
3. **Connect GitHub account** (처음 한 번만)
4. 저장소 목록에서 **CardNews** 선택
5. **Connect** 클릭

이제 아래 가이드를 따라 배포 설정을 진행하세요!
