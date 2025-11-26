"""
데이터베이스 연결 및 테이블 정의
SQLAlchemy를 사용하여 PostgreSQL과 연결합니다.
"""

from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# 기본 모델 클래스 (테이블 생성의 기반)
Base = declarative_base()


# ========== 예매 데이터 테이블 ==========
class Reservation(Base):
    """
    통합 예매 정보 테이블
    모든 예매처의 데이터가 이 테이블에 저장됩니다.
    """
    __tablename__ = 'reservations'
    
    # 고유 ID (자동 증가 번호)
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 공연 정보
    공연명 = Column(String(200), nullable=False)
    공연일 = Column(Date, nullable=False)
    회차정보 = Column(String(50))
    
    # 예매자 정보
    예매자 = Column(String(100))
    티켓번호 = Column(String(50), unique=True, nullable=False)  # 중복 방지
    좌석정보 = Column(String(100))
    가격 = Column(String(50))
    전화번호 = Column(String(50))
    
    # 예매처 정보
    출처 = Column(String(20), nullable=False)  # YES24, 인터파크, 티켓링크
    
    # 등록 시간 (자동 기록)
    생성일시 = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<예매 {self.티켓번호} - {self.공연명} ({self.출처})>"


# ========== 데이터베이스 연결 함수 ==========
def get_database_url():
    """환경 변수에서 데이터베이스 URL 가져오기"""
    return os.getenv('DATABASE_URL', 'sqlite:///ticket_local.db')


def init_db(database_url=None):
    """
    데이터베이스 초기화 및 테이블 생성
    
    Args:
        database_url: 데이터베이스 연결 주소 (없으면 환경 변수 사용)
    
    Returns:
        engine: 데이터베이스 엔진 객체
        Session: 세션 생성 클래스
    """
    if database_url is None:
        database_url = get_database_url()
    
    # 데이터베이스 엔진 생성
    engine = create_engine(database_url, echo=False)
    
    # 테이블 생성 (없을 경우에만)
    Base.metadata.create_all(engine)
    
    # 세션 생성기
    Session = sessionmaker(bind=engine)
    
    print(f"✅ 데이터베이스 연결 완료: {database_url[:30]}...")
    
    return engine, Session


def get_session():
    """
    새로운 데이터베이스 세션 생성
    데이터를 읽거나 쓸 때 사용합니다.
    """
    _, Session = init_db()
    return Session()
