from flask import Blueprint, request, jsonify, Response
from src.models.database import db
from src.models.user import User
from src.models.scavenger_step import ScavengerStep
from src.models.scan_event import ScanEvent
from src.models.admin_user import AdminUser
from src.routes.auth import verify_token
import json
import datetime

admin_bp = Blueprint('admin', __name__)

def require_admin_auth(f):
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        
        if not payload or not payload.get('is_admin'):
            return jsonify({'error': 'Admin access required'}), 403
        
        admin = AdminUser.query.get(payload['user_id'])
        if not admin:
            return jsonify({'error': 'Admin not found'}), 404
        
        return f(admin, *args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/users', methods=['GET'])
@require_admin_auth
def get_users(admin):
    try:
        users = User.query.order_by(User.created_at.desc()).all()
        users_data = []
        
        for user in users:
            user_data = user.to_dict()
            
            # Add additional stats
            completed_count = len(user.get_completed_steps())
            revealed_count = len(user.get_revealed_locations())
            
            # Get latest scan event
            latest_scan = ScanEvent.query.filter_by(user_id=user.id).order_by(ScanEvent.scanned_at.desc()).first()
            
            user_data.update({
                'completed_count': completed_count,
                'revealed_count': revealed_count,
                'latest_scan': latest_scan.to_dict() if latest_scan else None,
                'progress_percentage': round((completed_count / 13) * 100, 1)
            })
            
            users_data.append(user_data)
        
        return jsonify({'users': users_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/events', methods=['GET'])
@require_admin_auth
def get_events(admin):
    try:
        # Get query parameters for filtering
        user_id = request.args.get('user_id')
        step_id = request.args.get('step_id')
        success_only = request.args.get('success_only', 'false').lower() == 'true'
        limit = int(request.args.get('limit', 100))
        
        # Build query
        query = ScanEvent.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if step_id:
            query = query.filter_by(step_id=int(step_id))
        if success_only:
            query = query.filter_by(success=True)
        
        events = query.order_by(ScanEvent.scanned_at.desc()).limit(limit).all()
        
        events_data = []
        for event in events:
            event_data = event.to_dict()
            
            # Add user and step info
            user = User.query.get(event.user_id)
            step = ScavengerStep.query.get(event.step_id)
            
            event_data.update({
                'user_email': user.email if user else None,
                'user_phone': user.phone if user else None,
                'step_name': step.name if step else None
            })
            
            events_data.append(event_data)
        
        return jsonify({'events': events_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/user/<user_id>/reset', methods=['POST'])
@require_admin_auth
def reset_user_progress(admin, user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Reset user progress
        user.current_step = 1
        user.completed_steps = '[]'
        user.revealed_locations = '[]'
        user.last_active = datetime.datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'User progress reset successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/user/<user_id>/skip-step', methods=['POST'])
@require_admin_auth
def skip_step(admin, user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.current_step >= 13:
            return jsonify({'error': 'User has already completed all steps'}), 400
        
        # Mark current step as completed and move to next
        user.add_completed_step(user.current_step)
        user.current_step += 1
        user.last_active = datetime.datetime.utcnow()
        
        # Log admin action as scan event
        scan_event = ScanEvent(
            user_id=user.id,
            step_id=user.current_step - 1,
            success=True,
            revealed_first=False
        )
        db.session.add(scan_event)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Step skipped successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/steps/<int:step_id>', methods=['PUT'])
@require_admin_auth
def update_step(admin, step_id):
    try:
        step = ScavengerStep.query.get(step_id)
        if not step:
            return jsonify({'error': 'Step not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'qr_code_url' in data:
            step.qr_code_url = data['qr_code_url']
        if 'qr_code_value' in data:
            step.qr_code_value = data['qr_code_value']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Step updated successfully',
            'step': step.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/stats', methods=['GET'])
@require_admin_auth
def get_stats(admin):
    try:
        # Get overall statistics
        total_users = User.query.count()
        total_scans = ScanEvent.query.count()
        successful_scans = ScanEvent.query.filter_by(success=True).count()
        
        # Users who completed the hunt
        completed_users = 0
        for user in User.query.all():
            if len(user.get_completed_steps()) >= 13:
                completed_users += 1
        
        # Step completion rates
        step_stats = []
        for i in range(1, 14):
            step = ScavengerStep.query.get(i)
            if step:
                completed_count = 0
                revealed_count = 0
                
                for user in User.query.all():
                    completed_steps = user.get_completed_steps()
                    revealed_locations = user.get_revealed_locations()
                    
                    if i in completed_steps:
                        completed_count += 1
                    if i in revealed_locations:
                        revealed_count += 1
                
                step_stats.append({
                    'step_id': i,
                    'step_name': step.name,
                    'completed_count': completed_count,
                    'revealed_count': revealed_count,
                    'completion_rate': round((completed_count / total_users * 100), 1) if total_users > 0 else 0
                })
        
        return jsonify({
            'total_users': total_users,
            'total_scans': total_scans,
            'successful_scans': successful_scans,
            'completed_users': completed_users,
            'completion_rate': round((completed_users / total_users * 100), 1) if total_users > 0 else 0,
            'step_stats': step_stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/notifications/stream', methods=['GET'])
@require_admin_auth
def notification_stream(admin):
    def generate():
        # This is a simple implementation - in production, you'd use Redis or similar
        # For now, we'll just send a heartbeat every 30 seconds
        while True:
            yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': datetime.datetime.utcnow().isoformat()})}\n\n"
            import time
            time.sleep(30)
    
    return Response(generate(), mimetype='text/event-stream')

