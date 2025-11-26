#!/bin/bash
# 공연 예매 통합 관리 시스템 시작 스크립트

echo "======================================"
echo "🎭 공연 예매 통합 관리 시스템"
echo "======================================"
echo ""

# 데이터베이스 초기화 확인
if [ ! -f "ticket_database.db" ]; then
    echo "📊 데이터베이스 초기화 중..."
    python init_db.py
    echo ""
fi

# 서버 시작
echo "🚀 웹 서버 시작..."
echo "📍 주소: http://localhost:5000"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo "======================================"
echo ""

python app.py
