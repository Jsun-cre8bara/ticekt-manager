"""
전체 시스템 테스트 스크립트
모든 기능이 정상 작동하는지 자동으로 확인합니다.
"""

import sys
import os
from datetime import date

# 색상 코드
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    """헤더 출력"""
    print(f"\n{BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    """성공 메시지"""
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    """실패 메시지"""
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    """경고 메시지"""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    """정보 메시지"""
    print(f"{BLUE}ℹ️  {text}{RESET}")


# ========== 테스트 1: 환경 확인 ==========
def test_environment():
    """환경 설정 확인"""
    print_header("TEST 1: 환경 설정 확인")
    
    passed = 0
    failed = 0
    
    # Python 버전
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python 버전: {version.major}.{version.minor}.{version.micro}")
        passed += 1
    else:
        print_error(f"Python 버전 낮음: {version.major}.{version.minor}.{version.micro} (3.11+ 필요)")
        failed += 1
    
    # 필수 파일 존재 확인
    required_files = [
        'app.py',
        'database.py',
        'parser_web.py',
        'requirements.txt',
        '.env'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print_success(f"파일 존재: {file}")
            passed += 1
        else:
            print_error(f"파일 없음: {file}")
            failed += 1
    
    # .env 파일 확인
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            print_success(f"DATABASE_URL 설정됨: {db_url[:30]}...")
            passed += 1
        else:
            print_error("DATABASE_URL이 .env에 없음")
            failed += 1
    
    return passed, failed


# ========== 테스트 2: 라이브러리 확인 ==========
def test_libraries():
    """필수 라이브러리 설치 확인"""
    print_header("TEST 2: 라이브러리 설치 확인")
    
    passed = 0
    failed = 0
    
    libraries = [
        ('flask', 'Flask'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('pandas', 'Pandas'),
        ('openpyxl', 'Openpyxl'),
        ('dotenv', 'python-dotenv')
    ]
    
    for module_name, display_name in libraries:
        try:
            __import__(module_name)
            print_success(f"{display_name} 설치됨")
            passed += 1
        except ImportError:
            print_error(f"{display_name} 미설치")
            failed += 1
    
    return passed, failed


# ========== 테스트 3: 데이터베이스 ==========
def test_database():
    """데이터베이스 연결 및 테이블 확인"""
    print_header("TEST 3: 데이터베이스 확인")
    
    passed = 0
    failed = 0
    
    try:
        from database import init_db, get_session, Reservation
        from sqlalchemy import inspect
        
        # 연결 테스트
        engine, Session = init_db()
        print_success("데이터베이스 연결 성공")
        passed += 1
        
        # 테이블 확인
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'reservations' in tables:
            print_success("reservations 테이블 존재")
            passed += 1
            
            # 컬럼 확인
            columns = [col['name'] for col in inspector.get_columns('reservations')]
            required_columns = ['id', '공연명', '공연일', '티켓번호', '출처']
            
            for col in required_columns:
                if col in columns:
                    print_success(f"  컬럼 존재: {col}")
                    passed += 1
                else:
                    print_error(f"  컬럼 없음: {col}")
                    failed += 1
        else:
            print_error("reservations 테이블 없음")
            failed += 1
        
        # 데이터 개수 확인
        session = get_session()
        count = session.query(Reservation).count()
        print_info(f"현재 데이터: {count}개")
        session.close()
        
    except Exception as e:
        print_error(f"데이터베이스 오류: {e}")
        failed += 1
    
    return passed, failed


# ========== 테스트 4: 파서 기능 ==========
def test_parsers():
    """파서 함수 테스트"""
    print_header("TEST 4: 파서 기능 확인")
    
    passed = 0
    failed = 0
    
    try:
        from parser_web import 공연명정규화
        
        # 정규화 테스트
        test_cases = [
            ('〈공연명〉', '(공연명)'),
            ('[공연명]', '(공연명)'),
            ('【공연명】', '(공연명)'),
        ]
        
        for input_text, expected in test_cases:
            result = 공연명정규화(input_text)
            if result == expected:
                print_success(f"정규화: '{input_text}' → '{result}'")
                passed += 1
            else:
                print_error(f"정규화 실패: '{input_text}' → '{result}' (기대값: '{expected}')")
                failed += 1
        
        # 파서 함수 존재 확인
        from parser_web import parse_yes24, parse_interpark, parse_ticketlink
        print_success("parse_yes24 함수 존재")
        print_success("parse_interpark 함수 존재")
        print_success("parse_ticketlink 함수 존재")
        passed += 3
        
    except Exception as e:
        print_error(f"파서 오류: {e}")
        failed += 1
    
    return passed, failed


# ========== 테스트 5: Flask 앱 ==========
def test_flask_app():
    """Flask 앱 설정 확인"""
    print_header("TEST 5: Flask 앱 확인")
    
    passed = 0
    failed = 0
    
    try:
        from app import app
        
        # 앱 설정 확인
        if app.config.get('SECRET_KEY'):
            print_success("SECRET_KEY 설정됨")
            passed += 1
        else:
            print_error("SECRET_KEY 없음")
            failed += 1
        
        # 라우트 확인
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        
        required_routes = [
            '/',
            '/upload',
            '/reservations',
            '/api/upload/<vendor>',
            '/api/stats',
            '/api/export/excel'
        ]
        
        for route in required_routes:
            if route in routes:
                print_success(f"라우트 존재: {route}")
                passed += 1
            else:
                print_error(f"라우트 없음: {route}")
                failed += 1
        
    except Exception as e:
        print_error(f"Flask 앱 오류: {e}")
        failed += 1
    
    return passed, failed


# ========== 테스트 6: 템플릿 파일 ==========
def test_templates():
    """HTML 템플릿 파일 확인"""
    print_header("TEST 6: 템플릿 파일 확인")
    
    passed = 0
    failed = 0
    
    templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/upload.html',
        'templates/reservations.html'
    ]
    
    for template in templates:
        if os.path.exists(template):
            print_success(f"템플릿 존재: {template}")
            passed += 1
        else:
            print_error(f"템플릿 없음: {template}")
            failed += 1
    
    return passed, failed


# ========== 테스트 7: 배포 파일 ==========
def test_deployment_files():
    """배포 관련 파일 확인"""
    print_header("TEST 7: 배포 파일 확인")
    
    passed = 0
    failed = 0
    
    deployment_files = [
        'Procfile',
        'runtime.txt',
        'railway.json',
        '.gitignore',
        'requirements.txt'
    ]
    
    for file in deployment_files:
        if os.path.exists(file):
            print_success(f"배포 파일 존재: {file}")
            passed += 1
        else:
            print_error(f"배포 파일 없음: {file}")
            failed += 1
    
    return passed, failed


# ========== 메인 실행 ==========
def main():
    """전체 테스트 실행"""
    print(f"\n{BLUE}{'='*60}")
    print("  🧪 공연 예매 통합 관리 시스템")
    print("     전체 시스템 테스트")
    print(f"{'='*60}{RESET}\n")
    
    total_passed = 0
    total_failed = 0
    
    # 모든 테스트 실행
    tests = [
        test_environment,
        test_libraries,
        test_database,
        test_parsers,
        test_flask_app,
        test_templates,
        test_deployment_files
    ]
    
    for test_func in tests:
        try:
            passed, failed = test_func()
            total_passed += passed
            total_failed += failed
        except Exception as e:
            print_error(f"테스트 실행 오류: {e}")
            total_failed += 1
    
    # 최종 결과
    print_header("최종 결과")
    
    total_tests = total_passed + total_failed
    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"총 테스트: {total_tests}개")
    print(f"{GREEN}통과: {total_passed}개{RESET}")
    
    if total_failed > 0:
        print(f"{RED}실패: {total_failed}개{RESET}")
    else:
        print(f"실패: 0개")
    
    print(f"성공률: {success_rate:.1f}%\n")
    
    # 결론
    if total_failed == 0:
        print(f"{GREEN}{'='*60}")
        print("  🎉 모든 테스트 통과!")
        print("     시스템이 정상적으로 작동합니다.")
        print(f"{'='*60}{RESET}\n")
        print_info("다음 단계: Railway 배포")
        print_info("가이드: QUICK_DEPLOY.md 또는 RAILWAY_DEPLOY_GUIDE.md")
        return 0
    else:
        print(f"{RED}{'='*60}")
        print("  ⚠️  일부 테스트 실패")
        print(f"     {total_failed}개 문제를 해결해주세요.")
        print(f"{'='*60}{RESET}\n")
        print_warning("문제 해결 가이드: LOCAL_TEST.md")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
