"""
데이터베이스 초기화 스크립트
처음 실행 시 데이터베이스와 테이블을 생성합니다.
"""

from database import init_db, get_session, Reservation, Base
from sqlalchemy import inspect
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def check_tables():
    """생성된 테이블 확인"""
    engine, _ = init_db()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n📊 생성된 테이블 목록:")
    for table in tables:
        print(f"  - {table}")
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"    └ {col['name']}: {col['type']}")
    
    return tables


def create_sample_data():
    """테스트용 샘플 데이터 생성"""
    session = get_session()
    
    try:
        # 기존 데이터 확인
        count = session.query(Reservation).count()
        if count > 0:
            print(f"\n⚠️  이미 {count}개의 데이터가 있습니다.")
            response = input("샘플 데이터를 추가하시겠습니까? (y/n): ")
            if response.lower() != 'y':
                return
        
        # 샘플 데이터
        from datetime import date
        
        samples = [
            Reservation(
                공연명="뮤지컬 위키드",
                공연일=date(2024, 12, 1),
                회차정보="1회차 14:00",
                예매자="홍길동",
                티켓번호="Y20241201001",
                좌석정보="1층 A구역 10열 5번",
                가격="99000",
                전화번호="010-1234-5678",
                출처="YES24"
            ),
            Reservation(
                공연명="뮤지컬 위키드",
                공연일=date(2024, 12, 1),
                회차정보="1회차 14:00",
                예매자="김철수",
                티켓번호="T20241201001",
                좌석정보="1층 B구역 12열 8번",
                가격="99000",
                전화번호="010-9876-5432",
                출처="인터파크"
            ),
            Reservation(
                공연명="뮤지컬 위키드",
                공연일=date(2024, 12, 1),
                회차정보="2회차 19:00",
                예매자="이영희",
                티켓번호="TL20241201001",
                좌석정보="2층 C구역 3열 15번",
                가격="77000",
                전화번호="010-5555-6666",
                출처="티켓링크"
            )
        ]
        
        # 데이터 추가
        for sample in samples:
            session.add(sample)
        
        session.commit()
        print(f"\n✅ 샘플 데이터 {len(samples)}개 추가 완료!")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ 오류 발생: {e}")
    finally:
        session.close()


def main():
    """메인 실행 함수"""
    print("="*60)
    print("🗄️  데이터베이스 초기화")
    print("="*60)
    
    # 환경 변수 확인
    db_url = os.getenv('DATABASE_URL', '설정 안됨')
    print(f"\n📍 데이터베이스 URL: {db_url[:50]}...")
    
    # 데이터베이스 초기화
    print("\n🔧 데이터베이스 및 테이블 생성 중...")
    engine, Session = init_db()
    
    # 테이블 확인
    tables = check_tables()
    
    if 'reservations' in tables:
        print(f"\n✅ 'reservations' 테이블 생성 완료!")
        
        # 샘플 데이터 추가 여부
        response = input("\n샘플 데이터를 추가하시겠습니까? (y/n): ")
        if response.lower() == 'y':
            create_sample_data()
    else:
        print("\n❌ 테이블 생성 실패!")
    
    print("\n" + "="*60)
    print("✨ 초기화 완료!")
    print("="*60)


if __name__ == "__main__":
    main()
