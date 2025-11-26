"""
데이터베이스 연결 테스트
데이터베이스가 제대로 연결되는지 확인합니다.
"""

from database import init_db, get_session, Reservation
from sqlalchemy import text
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def test_connection():
    """데이터베이스 연결 테스트"""
    print("="*60)
    print("🔍 데이터베이스 연결 테스트")
    print("="*60)
    
    # 환경 변수 확인
    db_url = os.getenv('DATABASE_URL', '설정 안됨')
    db_type = 'SQLite' if 'sqlite' in db_url else 'PostgreSQL'
    
    print(f"\n📍 데이터베이스 타입: {db_type}")
    print(f"📍 연결 URL: {db_url[:50]}...")
    
    try:
        # 연결 시도
        print("\n🔧 연결 시도 중...")
        engine, Session = init_db()
        
        # 세션 생성
        session = get_session()
        
        # 간단한 쿼리 실행
        print("🔧 쿼리 테스트 중...")
        
        if 'postgresql' in db_url:
            result = session.execute(text("SELECT version()")).fetchone()
            print(f"✅ PostgreSQL 버전: {result[0][:50]}...")
        else:
            result = session.execute(text("SELECT sqlite_version()")).fetchone()
            print(f"✅ SQLite 버전: {result[0]}")
        
        # 테이블 확인
        count = session.query(Reservation).count()
        print(f"✅ reservations 테이블 접근 성공!")
        print(f"   현재 데이터 개수: {count}개")
        
        session.close()
        
        print("\n" + "="*60)
        print("✨ 모든 테스트 통과!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("\n💡 해결 방법:")
        print("  1. .env 파일이 있는지 확인")
        print("  2. DATABASE_URL이 올바른지 확인")
        print("  3. init_db.py를 먼저 실행했는지 확인")
        print("="*60)
        return False


if __name__ == "__main__":
    test_connection()
