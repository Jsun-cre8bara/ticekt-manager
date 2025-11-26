# ⚡ Railway 배포 빠른 체크리스트

이 체크리스트를 따라하면 30분 안에 배포할 수 있습니다!

---

## 🎯 배포 전 준비 (5분)

- [ ] GitHub 계정 있음
- [ ] Railway 계정 생성 (GitHub 로그인)
- [ ] Git 설치됨
- [ ] `ticket-manager` 폴더 다운로드 및 압축 해제

---

## 📤 GitHub 업로드 (10분)

### 1. GitHub에서 새 저장소 만들기
- [ ] https://github.com 접속
- [ ] New repository → 이름: `ticket-manager`
- [ ] Create repository

### 2. 코드 업로드
```bash
cd ticket-manager폴더경로
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/사용자명/ticket-manager.git
git push -u origin main
```
- [ ] GitHub에서 파일 업로드 확인

---

## 🚂 Railway 배포 (10분)

### 3. Railway 프로젝트 생성
- [ ] https://railway.app 접속
- [ ] New Project → Deploy from GitHub repo
- [ ] `ticket-manager` 저장소 선택

### 4. PostgreSQL 추가
- [ ] New → Database → Add PostgreSQL
- [ ] `DATABASE_URL` 자동 생성 확인

### 5. 환경 변수 설정
- [ ] Variables 탭 이동
- [ ] `SECRET_KEY` 추가 (아무 문자열)
- [ ] `FLASK_ENV` = `production`
- [ ] `DEBUG` = `False`

### 6. 데이터베이스 초기화
- [ ] PostgreSQL → Data → Query
- [ ] 다음 SQL 실행:
```sql
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    공연명 VARCHAR(200) NOT NULL,
    공연일 DATE NOT NULL,
    회차정보 VARCHAR(50),
    예매자 VARCHAR(100),
    티켓번호 VARCHAR(50) UNIQUE NOT NULL,
    좌석정보 VARCHAR(100),
    가격 VARCHAR(50),
    전화번호 VARCHAR(50),
    출처 VARCHAR(20) NOT NULL,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. 도메인 생성
- [ ] Settings → Networking → Generate Domain
- [ ] URL 복사

---

## ✅ 테스트 (5분)

### 8. 기능 확인
- [ ] 생성된 URL로 접속
- [ ] 홈페이지 표시됨
- [ ] 파일 업로드 테스트
- [ ] 통합 리스트 확인
- [ ] 엑셀 다운로드 테스트

---

## 🎉 완료!

배포 완료 URL: `_____________________.railway.app`

---

## 🚨 문제 발생 시

### 서버가 시작 안 됨
1. Deployments → View Logs 확인
2. DATABASE_URL 환경 변수 확인
3. Redeploy 클릭

### 데이터베이스 연결 실패
1. PostgreSQL 서비스 실행 중인지 확인
2. Variables에서 DATABASE_URL 확인
3. 테이블 생성했는지 확인

### 파일 업로드 실패
1. 로그에서 에러 확인
2. 엑셀 파일 형식 확인
3. 로컬에서 먼저 테스트

---

## 📝 메모

배포 날짜: ____________

배포 URL: ____________

문제 발생 시: RAILWAY_DEPLOY_GUIDE.md 참고
