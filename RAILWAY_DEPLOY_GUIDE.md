# 🚀 Railway 배포 완전 가이드

이 가이드를 따라하시면 프로젝트를 Railway에 배포하여 24시간 운영할 수 있습니다.

---

## 📋 사전 준비 (5분)

### 1. 필요한 계정
- ✅ **GitHub 계정** (코드 저장용)
  - 없으면 https://github.com 에서 무료 가입
- ✅ **Railway 계정** (배포용)
  - https://railway.app 에서 GitHub으로 로그인

### 2. 컴퓨터에 Git 설치
- Windows: https://git-scm.com/download/win
- Mac: Terminal에서 `git --version` (이미 설치됨)

---

## 🔧 STEP 1: GitHub에 코드 업로드 (10분)

### 1-1. GitHub에서 새 저장소 만들기

1. https://github.com 로그인
2. 우측 상단 **+** 버튼 → **New repository** 클릭
3. 저장소 설정:
   ```
   Repository name: ticket-manager
   Description: 공연 예매 통합 관리 시스템
   Public 또는 Private 선택
   ✅ Add a README file: 체크 안함!
   ```
4. **Create repository** 클릭

### 1-2. 로컬 프로젝트를 GitHub에 업로드

다운로드한 `ticket-manager` 폴더에서 다음 명령어를 실행하세요:

**Windows (명령 프롬프트 또는 PowerShell):**
```bash
cd C:\Users\사용자명\Downloads\ticket-manager
git init
git add .
git commit -m "Initial commit: 공연 예매 통합 관리 시스템"
git branch -M main
git remote add origin https://github.com/사용자명/ticket-manager.git
git push -u origin main
```

**Mac/Linux (터미널):**
```bash
cd ~/Downloads/ticket-manager
git init
git add .
git commit -m "Initial commit: 공연 예매 통합 관리 시스템"
git branch -M main
git remote add origin https://github.com/사용자명/ticket-manager.git
git push -u origin main
```

> 💡 **주의**: `https://github.com/사용자명/ticket-manager.git` 부분을 
> 자신의 GitHub 저장소 주소로 변경하세요!

### 1-3. GitHub에서 업로드 확인

- 브라우저에서 자신의 저장소로 이동
- 파일들이 모두 올라갔는지 확인

---

## 🚂 STEP 2: Railway 프로젝트 생성 (5분)

### 2-1. Railway 로그인

1. https://railway.app 접속
2. **Login** → **Login with GitHub** 클릭
3. GitHub 계정으로 로그인

### 2-2. 새 프로젝트 생성

1. 대시보드에서 **+ New Project** 클릭
2. **Deploy from GitHub repo** 선택
3. **Configure GitHub App** 클릭 (처음이면)
4. Repository access 설정:
   - **Only select repositories** 선택
   - `ticket-manager` 저장소 선택
   - **Save** 클릭
5. Railway로 돌아와서 `ticket-manager` 저장소 선택

### 2-3. 자동 배포 시작

- Railway가 자동으로 코드를 읽고 배포 시작
- **Deployments** 탭에서 진행 상황 확인
- 처음엔 빌드만 되고 실행은 안 됨 (데이터베이스 필요)

---

## 🗄️ STEP 3: PostgreSQL 데이터베이스 추가 (3분)

### 3-1. 데이터베이스 서비스 추가

1. 프로젝트 화면에서 **+ New** 버튼 클릭
2. **Database** 선택
3. **Add PostgreSQL** 클릭

### 3-2. 자동 연결 확인

- PostgreSQL이 추가되면 자동으로 `DATABASE_URL` 환경 변수 생성됨
- **Variables** 탭에서 확인 가능

---

## ⚙️ STEP 4: 환경 변수 설정 (2분)

### 4-1. 환경 변수 추가

1. 프로젝트에서 웹 서비스 선택 (ticket-manager)
2. **Variables** 탭 클릭
3. 다음 변수들을 추가:

```bash
# 1. SECRET_KEY (랜덤 문자열)
SECRET_KEY=your-super-secret-random-key-123456

# 2. FLASK_ENV
FLASK_ENV=production

# 3. DEBUG
DEBUG=False
```

> 💡 **SECRET_KEY**는 아무 문자열이나 넣으셔도 되지만, 
> 길고 복잡할수록 안전합니다!

### 4-2. DATABASE_URL 확인

- `DATABASE_URL`이 자동으로 있는지 확인
- 있으면 OK, 없으면 PostgreSQL 재연결

---

## 🎯 STEP 5: 데이터베이스 초기화 (5분)

### 5-1. Railway CLI 설치 (선택 사항)

**방법 A: 웹 콘솔 사용 (추천)**
1. Railway 프로젝트에서 서비스 선택
2. **Settings** 탭
3. 아래로 스크롤하여 **Service** 섹션
4. **Enable Railway CLI** 옵션 확인

**방법 B: 로컬에서 CLI 설치**
```bash
# Mac/Linux
brew install railway

# Windows
npm install -g @railway/cli
```

### 5-2. 데이터베이스 테이블 생성

**웹 콘솔 방법:**
1. Railway 프로젝트 → PostgreSQL 서비스 선택
2. **Data** 탭 → **Query** 클릭
3. 다음 SQL 실행:

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

**또는 CLI 방법:**
```bash
railway login
railway link
railway run python init_db.py
```

---

## 🌐 STEP 6: 배포 완료 및 접속 (2분)

### 6-1. 배포 상태 확인

1. **Deployments** 탭에서 최신 배포 확인
2. 상태가 **SUCCESS** 또는 **ACTIVE**인지 확인
3. 로그에서 에러 없는지 확인:
   ```
   🎭 공연 예매 통합 관리 시스템
   ✅ 데이터베이스 연결 완료
   ```

### 6-2. 공개 URL 설정

1. **Settings** 탭
2. **Networking** 섹션
3. **Generate Domain** 클릭
4. 자동으로 URL 생성됨 (예: `your-app.railway.app`)

### 6-3. 웹사이트 접속

1. 생성된 URL 클릭 또는 복사
2. 브라우저에서 접속
3. 홈페이지가 나타나면 성공! 🎉

---

## ✅ STEP 7: 기능 테스트 (5분)

### 7-1. 홈페이지 확인
- [ ] 통계가 "0"으로 표시되는가?
- [ ] 메뉴가 정상 작동하는가?

### 7-2. 파일 업로드 테스트
1. **파일 업로드** 메뉴 클릭
2. 테스트용 엑셀 파일 업로드
3. 처리 결과 확인

### 7-3. 통합 리스트 확인
1. **통합 리스트** 메뉴 클릭
2. 업로드한 데이터 표시 확인
3. 검색/필터 기능 테스트
4. 엑셀 다운로드 테스트

---

## 🔧 문제 해결

### ❌ "Application failed to respond" 에러

**원인**: 서버가 시작되지 않음

**해결**:
1. **Deployments** → **View Logs** 확인
2. 에러 메시지 확인
3. 데이터베이스 연결 문제일 가능성:
   - `DATABASE_URL` 환경 변수 확인
   - PostgreSQL 서비스 실행 중인지 확인

### ❌ 데이터베이스 연결 실패

**원인**: `DATABASE_URL`이 없거나 잘못됨

**해결**:
1. **Variables** 탭에서 `DATABASE_URL` 확인
2. 없으면 PostgreSQL 서비스 재시작
3. 있는데 안 되면 서비스 재배포:
   - **Deployments** → **Redeploy** 클릭

### ❌ 파일 업로드 실패

**원인**: 파서 오류 또는 파일 형식 문제

**해결**:
1. 로그에서 에러 메시지 확인
2. 엑셀 파일 형식 확인 (.xlsx, .xls)
3. 로컬에서 테스트:
   ```bash
   python test_parser.py
   ```

### ❌ 502 Bad Gateway

**원인**: 서버가 응답하지 않음

**해결**:
1. **Settings** → **Restart** 클릭
2. 로그 확인
3. 메모리 부족일 수 있음 (무료 플랜 제한)

---

## 📊 Railway 무료 플랜 제한

### 제공 내용
- ✅ 500시간/월 실행 시간
- ✅ 512MB RAM
- ✅ 1GB 디스크
- ✅ PostgreSQL 데이터베이스

### 주의사항
- 활동 없으면 일시 정지 (다시 접속하면 자동 재시작)
- 많은 데이터 저장 시 업그레이드 필요
- 24시간 상시 운영하려면 약 17일 사용 가능

### 비용 절약 팁
- 사용하지 않을 때는 일시 정지
- 필요할 때만 실행
- 로컬 테스트 후 배포

---

## 🎓 다음 단계

### 배포 완료 후
1. ✅ URL을 팀원들과 공유
2. ✅ 실제 예매 파일로 테스트
3. ✅ 데이터 백업 주기적으로

### 업데이트 방법
```bash
# 로컬에서 코드 수정 후
git add .
git commit -m "업데이트 내용"
git push

# Railway가 자동으로 재배포!
```

---

## 📞 추가 도움말

### Railway 공식 문서
- https://docs.railway.app

### GitHub 도움말
- https://docs.github.com

### 문제 발생 시
1. Railway 로그 확인
2. 로컬에서 테스트
3. 환경 변수 재확인

---

**🎉 축하합니다!**

이제 여러분의 공연 예매 통합 관리 시스템이 인터넷에서 24시간 운영됩니다!

---

**작성일**: 2024-11-26
