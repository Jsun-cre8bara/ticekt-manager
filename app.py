"""
공연 예매 통합 관리 시스템
Flask 웹 애플리케이션 메인 파일
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from database import init_db, get_session, Reservation

# 환경 변수 로드
load_dotenv()

# Flask 앱 생성
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 데이터베이스 초기화
engine, Session = init_db()


# ========== 메인 페이지 ==========
@app.route('/')
def index():
    """홈페이지"""
    return render_template('index.html')


# ========== 파일 업로드 페이지 ==========
@app.route('/upload')
def upload_page():
    """파일 업로드 페이지"""
    return render_template('upload.html')


# ========== 통합 리스트 조회 페이지 ==========
@app.route('/reservations')
def reservations():
    """통합 예매 리스트 조회"""
    session = get_session()
    try:
        # 모든 예매 데이터 가져오기 (최신순)
        all_reservations = session.query(Reservation).order_by(
            Reservation.공연일.desc(),
            Reservation.생성일시.desc()
        ).all()
        
        return render_template('reservations.html', reservations=all_reservations)
    finally:
        session.close()


# ========== API: 파일 업로드 처리 ==========
@app.route('/api/upload/<vendor>', methods=['POST'])
def upload_file(vendor):
    """
    예매처별 파일 업로드 처리
    
    Args:
        vendor: 예매처 이름 (yes24, interpark, ticketlink)
    """
    # 파일 확인
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '파일이 없습니다.'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '파일이 선택되지 않았습니다.'}), 400
    
    # 엑셀 파일 확인
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'success': False, 'message': '엑셀 파일만 업로드 가능합니다.'}), 400
    
    try:
        # 파일 저장
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 파서 함수 호출
        from parser_web import process_file
        
        결과 = process_file(filepath, vendor)
        
        # 업로드된 파일 삭제 (데이터베이스에 저장됨)
        os.remove(filepath)
        
        if 결과['success']:
            return jsonify({
                'success': True,
                'message': f'{vendor.upper()} 파일 처리 완료!',
                'stats': {
                    '전체': 결과.get('전체', 0),
                    '성공': 결과.get('성공', 0),
                    '중복': 결과.get('중복', 0),
                    '실패': 결과.get('실패', 0)
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 결과.get('error', '알 수 없는 오류')
            }), 400
    
    except Exception as e:
        # 에러 발생 시 파일 삭제
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'success': False, 'message': f'오류 발생: {str(e)}'}), 500


# ========== API: 통계 정보 ==========
@app.route('/api/stats')
def get_stats():
    """전체 통계 정보 반환"""
    session = get_session()
    try:
        total = session.query(Reservation).count()
        
        # 예매처별 카운트
        yes24_count = session.query(Reservation).filter_by(출처='YES24').count()
        interpark_count = session.query(Reservation).filter_by(출처='인터파크').count()
        ticketlink_count = session.query(Reservation).filter_by(출처='티켓링크').count()
        
        return jsonify({
            'total': total,
            'yes24': yes24_count,
            'interpark': interpark_count,
            'ticketlink': ticketlink_count
        })
    finally:
        session.close()


# ========== API: 개별 예매 삭제 ==========
@app.route('/api/reservation/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    """개별 예매 데이터 삭제"""
    session = get_session()
    try:
        reservation = session.query(Reservation).filter_by(id=reservation_id).first()
        
        if not reservation:
            return jsonify({'success': False, 'message': '예매를 찾을 수 없습니다.'}), 404
        
        session.delete(reservation)
        session.commit()
        
        return jsonify({'success': True, 'message': '삭제되었습니다.'})
    
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        session.close()


# ========== API: 전체 예매 삭제 ==========
@app.route('/api/reservations/delete-all', methods=['DELETE'])
def delete_all_reservations():
    """모든 예매 데이터 삭제"""
    session = get_session()
    try:
        count = session.query(Reservation).count()
        session.query(Reservation).delete()
        session.commit()
        
        return jsonify({
            'success': True, 
            'message': '모든 데이터가 삭제되었습니다.',
            'deleted': count
        })
    
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        session.close()


# ========== API: 엑셀 다운로드 ==========
@app.route('/api/export/excel')
def export_excel():
    """예매 데이터를 엑셀 파일로 다운로드"""
    session = get_session()
    try:
        # 모든 예매 데이터 가져오기
        reservations = session.query(Reservation).order_by(
            Reservation.공연일.desc(),
            Reservation.출처
        ).all()
        
        if not reservations:
            flash('다운로드할 데이터가 없습니다.', 'warning')
            return redirect(url_for('reservations'))
        
        # 데이터프레임 생성
        import pandas as pd
        from datetime import datetime
        
        data = []
        for r in reservations:
            data.append({
                '공연명': r.공연명,
                '공연일': str(r.공연일),
                '회차(공연시간)': r.회차정보,
                '예매자 이름': r.예매자,
                '예매번호': r.티켓번호,
                '좌석정보': r.좌석정보,
                '구매가격': r.가격,
                '예매자 연락처': r.전화번호,
                '예매처': r.출처
            })
        
        df = pd.DataFrame(data)
        
        # 엑셀 파일 생성
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'export_temp.xlsx')
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        # 파일명 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'예매통합장부_{timestamp}.xlsx'
        
        # 파일 전송
        from flask import send_file
        response = send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        # 임시 파일 삭제 (응답 후)
        @response.call_on_close
        def cleanup():
            try:
                os.remove(output_path)
            except:
                pass
        
        return response
    
    except Exception as e:
        flash(f'다운로드 실패: {str(e)}', 'danger')
        return redirect(url_for('reservations'))
    finally:
        session.close()


# ========== 앱 실행 ==========
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎭 공연 예매 통합 관리 시스템")
    print("="*50)
    print(f"📍 서버 주소: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
