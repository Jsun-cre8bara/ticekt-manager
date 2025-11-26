"""
파서 웹 모듈 테스트
샘플 데이터를 생성하여 파서가 제대로 작동하는지 확인
"""

from database import get_session, Reservation
from datetime import date

def create_test_data():
    """테스트용 샘플 데이터 생성"""
    session = get_session()
    
    print("="*60)
    print("🧪 테스트 데이터 생성")
    print("="*60)
    
    try:
        # 기존 데이터 확인
        count = session.query(Reservation).count()
        print(f"\n현재 데이터: {count}개")
        
        if count > 0:
            response = input("\n기존 데이터를 모두 삭제하고 테스트 데이터를 추가하시겠습니까? (y/n): ")
            if response.lower() == 'y':
                session.query(Reservation).delete()
                session.commit()
                print("✅ 기존 데이터 삭제 완료")
            else:
                print("취소되었습니다.")
                return
        
        # 테스트 데이터
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
            ),
            Reservation(
                공연명="연극 햄릿",
                공연일=date(2024, 12, 5),
                회차정보="1회차 20:00",
                예매자="박민수",
                티켓번호="Y20241205001",
                좌석정보="R석 5열 10번",
                가격="50000",
                전화번호="010-1111-2222",
                출처="YES24"
            ),
            Reservation(
                공연명="콘서트 BTS",
                공연일=date(2024, 12, 10),
                회차정보="1회차 19:00",
                예매자="최지민",
                티켓번호="T20241210001",
                좌석정보="스탠딩 A구역",
                가격="150000",
                전화번호="010-3333-4444",
                출처="인터파크"
            )
        ]
        
        for sample in samples:
            session.add(sample)
        
        session.commit()
        
        print(f"\n✅ 테스트 데이터 {len(samples)}개 추가 완료!")
        print("\n📊 추가된 데이터:")
        for s in samples:
            print(f"  - {s.공연명} | {s.예매자} | {s.출처}")
        
        print("\n" + "="*60)
        print("✨ 테스트 데이터 생성 완료!")
        print("="*60)
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ 오류 발생: {e}")
    finally:
        session.close()


def view_all_data():
    """모든 데이터 조회"""
    session = get_session()
    
    print("\n" + "="*60)
    print("📋 전체 예매 데이터")
    print("="*60)
    
    try:
        reservations = session.query(Reservation).order_by(
            Reservation.공연일.desc(),
            Reservation.출처
        ).all()
        
        if not reservations:
            print("\n데이터가 없습니다.")
        else:
            print(f"\n총 {len(reservations)}개의 예매")
            print("\n" + "-"*60)
            
            for r in reservations:
                print(f"[{r.출처:6}] {r.공연명:15} | {r.공연일} | {r.예매자:8} | {r.티켓번호}")
        
        print("-"*60)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'view':
        view_all_data()
    else:
        create_test_data()
        view_all_data()
