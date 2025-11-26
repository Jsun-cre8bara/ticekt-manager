# 🚀 Railway 배포 가이드

이 문서는 프로젝트를 Railway에 배포하는 방법을 설명합니다.

## 📋 사전 준비

1. **Railway 계정** 생성
   - https://railway.app 접속
   - GitHub 계정으로 로그인

2. **GitHub 계정** (코드 업로드용)
   - https://github.com 계정 필요

## 🔧 배포 단계

### 1단계: GitHub에 코드 업로드

```bash
# 프로젝트 폴더에서 실행
git init
git add .
git commit -m "Initial commit"

# GitHub에 새 저장소 생성 후
git remote add origin https://github.com/사용자명/저장소명.git
git push -u origin main
```

### 2단계: Railway 프로젝트 생성

1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. 본인의 GitHub 저장소 선택

### 3단계: PostgreSQL 데이터베이스 추가

1. Railway 프로젝트에서 "New" → "Database" → "PostgreSQL" 선택
2. 자동으로 DATABASE_URL 환경 변수 생성됨

### 4단계: 환경 변수 설정

Railway 프로젝트 설정에서 다음 변수 추가:

```
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production
DEBUG=False
```

### 5단계: 배포 확인

- Railway가 자동으로 앱을 빌드하고 배포
- "Deployments" 탭에서 로그 확인
- 배포 완료 후 제공되는 URL로 접속

## 🗄️ 데이터베이스 초기화

배포 후 Railway 콘솔에서 실행:

```bash
python init_db.py
```

## ⚙️ 주요 파일 설명

- **Procfile**: Railway에게 앱 실행 방법 알림
- **runtime.txt**: Python 버전 지정
- **railway.json**: Railway 설정
- **.env**: 로컬 환경 변수 (Railway에는 업로드 안됨)
- **.gitignore**: Git에 업로드하지 않을 파일 목록

## 🔍 문제 해결

### 데이터베이스 연결 실패
- Railway에서 PostgreSQL 서비스가 실행 중인지 확인
- DATABASE_URL 환경 변수 확인

### 앱이 시작되지 않음
- Railway 로그에서 오류 메시지 확인
- requirements.txt의 라이브러리 버전 확인

## 📞 참고 링크

- Railway 공식 문서: https://docs.railway.app
- Flask 배포 가이드: https://flask.palletsprojects.com/en/3.0.x/deploying/

---

**작성일**: 2024-11-26
