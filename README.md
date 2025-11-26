# 🎭 공연 예매 통합 관리 시스템

여러 예매처(YES24, 인터파크, 티켓링크)의 예매 데이터를 웹에서 관리하는 시스템입니다.

## 📋 주요 기능

✅ **예매처별 파일 업로드**
- YES24, 인터파크, 티켓링크 엑셀 파일 지원
- 자동 데이터 파싱 및 검증
- 중복 데이터 자동 감지

✅ **통합 데이터 관리**
- 모든 예매처 데이터를 하나의 데이터베이스에 저장
- 티켓번호 기준 중복 방지
- 실시간 통계 대시보드

✅ **강력한 검색 및 필터**
- 키워드 검색 (공연명, 예매자, 티켓번호)
- 예매처별 필터링
- 날짜 범위 필터링
- 실시간 결과 업데이트

✅ **데이터 관리**
- 개별 예매 삭제
- 전체 데이터 삭제
- 엑셀 파일로 다운로드

✅ **상시 운영**
- Railway 배포 지원
- PostgreSQL 데이터베이스
- 24시간 서비스 가능

## 🛠️ 기술 스택

- **웹 프레임워크**: Flask
- **데이터베이스**: PostgreSQL
- **프론트엔드**: Bootstrap 5
- **배포**: Railway

## 📁 프로젝트 구조

```
ticket-manager/
├── app.py              # 메인 웹 서버
├── database.py         # 데이터베이스 관리
├── requirements.txt    # 필요 라이브러리
├── .env.example        # 환경 변수 예시
├── parsers/           # 예매처별 파서
│   ├── YES24_파서.py
│   ├── 인터파크_파서.py
│   └── 티켓링크_파서.py
└── templates/         # HTML 페이지
    ├── base.html
    └── index.html
```

## 🚀 설치 및 실행 방법

### 1. 필요 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 열어서 DATABASE_URL 수정 (기본값은 SQLite 사용)
```

### 3. 데이터베이스 초기화
```bash
python init_db.py
```
- 처음 실행 시 데이터베이스와 테이블 자동 생성
- 샘플 데이터 추가 가능 (선택 사항)

### 4. 데이터베이스 연결 테스트 (선택)
```bash
python test_db.py
```

### 5. 서버 실행
```bash
python app.py
```

### 6. 브라우저에서 접속
```
http://localhost:5000
```

## 📝 다음 단계

모든 기능이 완성되었습니다! ✨

### 📄 페이지 구성
1. **홈페이지** (`/`) - 시스템 개요 및 통계 대시보드
2. **파일 업로드** (`/upload`) - 예매처별 엑셀 파일 업로드
3. **통합 리스트** (`/reservations`) - 전체 예매 데이터 조회 및 관리

### 📚 문서 가이드

**시작하기**
- `LOCAL_TEST.md` - 로컬에서 테스트하는 방법 (5분)
- `QUICK_DEPLOY.md` - 30분 만에 Railway 배포하기 (체크리스트)
- `RAILWAY_DEPLOY_GUIDE.md` - Railway 배포 완전 가이드 (상세)

**참고 문서**
- `CHECKLIST.md` - 완성된 기능 목록
- `DEPLOY.md` - Railway 배포 개요

### 🎯 추천 순서

1. **로컬 테스트** → `LOCAL_TEST.md` 참고
2. **Railway 배포** → `QUICK_DEPLOY.md` 체크리스트 따라하기
3. **실제 사용** → 예매 파일 업로드 및 관리

### 📞 문제 발생 시
- 로컬 테스트: `LOCAL_TEST.md`의 문제 해결 섹션
- Railway 배포: `RAILWAY_DEPLOY_GUIDE.md`의 문제 해결 섹션
- Railway 로그 확인: Deployments → View Logs

---

**작성일**: 2024-11-26
