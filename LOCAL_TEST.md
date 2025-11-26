# 💻 로컬 테스트 가이드

Railway에 배포하기 전에 자신의 컴퓨터에서 먼저 테스트해보세요!

---

## 📋 사전 준비

### 필요한 프로그램
- **Python 3.11 이상**
  - Windows: https://www.python.org/downloads/
  - Mac: 기본 설치되어 있음 (`python3 --version`으로 확인)
  - 설치 시 "Add Python to PATH" 체크!

---

## 🚀 실행 방법

### STEP 1: 폴더 이동

**Windows (명령 프롬프트):**
```cmd
cd C:\Users\사용자명\Downloads\ticket-manager
```

**Mac/Linux (터미널):**
```bash
cd ~/Downloads/ticket-manager
```

### STEP 2: 라이브러리 설치

**Windows:**
```cmd
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

> ⏱️ 약 1~2분 소요

### STEP 3: 데이터베이스 초기화

**Windows:**
```cmd
python init_db.py
```

**Mac/Linux:**
```bash
python3 init_db.py
```

질문이 나오면:
- "샘플 데이터를 추가하시겠습니까?" → `y` 입력

### STEP 4: 웹 서버 실행

**방법 A: 시작 스크립트 사용 (추천)**

**Windows:**
```cmd
python app.py
```

**Mac/Linux:**
```bash
./start.sh
또는
python3 app.py
```

**방법 B: 직접 실행**
```bash
python app.py
```

### STEP 5: 브라우저로 접속

서버가 시작되면 다음과 같이 표시됩니다:
```
==================================================
🎭 공연 예매 통합 관리 시스템
==================================================
📍 서버 주소: http://localhost:5000
==================================================
```

브라우저에서 접속:
```
http://localhost:5000
```

---

## ✅ 테스트 항목

### 1. 홈페이지 확인
- [ ] 페이지가 정상 표시됨
- [ ] 통계 숫자가 보임 (샘플 데이터: 5개)
- [ ] 메뉴 클릭 가능

### 2. 파일 업로드 테스트
- [ ] 파일 업로드 페이지 접속
- [ ] 각 예매처별 업로드 영역 표시
- [ ] 테스트 엑셀 파일 업로드
- [ ] 처리 결과 통계 표시

### 3. 통합 리스트 확인
- [ ] 리스트 페이지 접속
- [ ] 예매 데이터 테이블 표시
- [ ] 검색 기능 작동
- [ ] 필터 기능 작동
- [ ] 엑셀 다운로드 작동
- [ ] 개별 삭제 작동
- [ ] 전체 삭제 작동

---

## 🛠️ 유틸리티 명령어

### 데이터베이스 연결 테스트
```bash
python test_db.py
```

### 샘플 데이터 추가/확인
```bash
# 샘플 데이터 추가
python test_parser.py

# 데이터만 확인
python test_parser.py view
```

### 서버 종료
- **Ctrl + C** 키를 누르면 서버 종료

---

## 🐛 문제 해결

### ❌ "python: command not found"

**원인**: Python이 설치되지 않았거나 PATH에 없음

**해결**:
- Python 설치 확인: https://www.python.org
- Mac/Linux는 `python3` 사용

### ❌ "ModuleNotFoundError: No module named 'flask'"

**원인**: 라이브러리가 설치되지 않음

**해결**:
```bash
pip install -r requirements.txt
```

### ❌ "Address already in use"

**원인**: 5000번 포트가 이미 사용 중

**해결**:
1. 다른 Flask 앱이 실행 중인지 확인
2. 포트 변경:
   - `app.py` 열기
   - 마지막 줄 `port=5000`을 `port=5001`로 변경
   - `http://localhost:5001`로 접속

### ❌ "sqlite3.OperationalError: database is locked"

**원인**: 데이터베이스 파일이 다른 프로그램에서 사용 중

**해결**:
1. 모든 터미널/명령 프롬프트 창 닫기
2. `ticket_database.db` 파일 삭제
3. `python init_db.py` 다시 실행

---

## 📁 생성되는 파일

로컬 테스트 중 생성되는 파일들:

```
ticket-manager/
├── ticket_database.db      ← SQLite 데이터베이스 (로컬용)
├── uploads/                 ← 업로드된 파일 임시 저장
└── __pycache__/            ← Python 캐시 (무시)
```

> 💡 이 파일들은 로컬 테스트용이며, Railway 배포 시에는 사용되지 않습니다.

---

## 🔄 개발 워크플로우

### 코드 수정 후 테스트
1. 서버 종료 (Ctrl + C)
2. 코드 수정
3. 서버 재시작 (`python app.py`)
4. 브라우저 새로고침

### 데이터베이스 초기화
```bash
# 기존 데이터 삭제하고 새로 시작
rm ticket_database.db
python init_db.py
```

---

## 🎓 다음 단계

로컬 테스트가 성공했다면:

1. ✅ 모든 기능 정상 작동 확인
2. ✅ Railway 배포 진행
   - `RAILWAY_DEPLOY_GUIDE.md` 참고
   - `QUICK_DEPLOY.md`에서 체크리스트 확인

---

## 💡 팁

### 개발 모드 vs 운영 모드

**로컬 (개발 모드)**
- SQLite 데이터베이스 사용
- DEBUG=True (에러 상세 표시)
- 코드 수정 시 자동 재시작

**Railway (운영 모드)**
- PostgreSQL 데이터베이스 사용
- DEBUG=False (에러 간단히 표시)
- 배포 시에만 재시작

---

**작성일**: 2024-11-26
