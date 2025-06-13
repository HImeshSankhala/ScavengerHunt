from flask import Blueprint, request, jsonify
from src.models.database import db
from src.models.user import User
from src.models.scavenger_step import ScavengerStep
from src.models.scan_event import ScanEvent
from src.routes.auth import verify_token
import datetime

hunt_bp = Blueprint('hunt', __name__)

def require_auth(f):
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        
        if not payload or payload.get('is_admin'):
            return jsonify({'error': 'Invalid token'}), 401
        
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return f(user, *args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@hunt_bp.route('/current-step', methods=['GET'])
@require_auth
def get_current_step(user):
    try:
        # Get current step
        current_step = ScavengerStep.query.get(user.current_step)
        if not current_step:
            return jsonify({'error': 'Step not found'}), 404
        
        # Check if user has completed all steps
        completed_steps = user.get_completed_steps()
        if len(completed_steps) >= 13:
            return jsonify({
                'completed': True,
                'message': 'Congratulations! You have completed the scavenger hunt!'
            }), 200
        
        return jsonify({
            'step': current_step.to_dict_for_user(),
            'progress': {
                'current': user.current_step,
                'total': 13,
                'completed_steps': completed_steps,
                'revealed_locations': user.get_revealed_locations()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hunt_bp.route('/scan-qr', methods=['POST'])
@require_auth
def scan_qr(user):
    try:
        data = request.get_json()
        qr_value = data.get('qr_value')
        
        if not qr_value:
            return jsonify({'error': 'QR value required'}), 400
        
        # Get current step
        current_step = ScavengerStep.query.get(user.current_step)
        if not current_step:
            return jsonify({'error': 'Current step not found'}), 404
        
        # Check if QR code matches current step
        success = qr_value == current_step.qr_code_value
        
        # Check if user revealed location first
        revealed_locations = user.get_revealed_locations()
        revealed_first = user.current_step in revealed_locations
        
        # Log scan event
        scan_event = ScanEvent(
            user_id=user.id,
            step_id=user.current_step,
            success=success,
            revealed_first=revealed_first
        )
        db.session.add(scan_event)
        
        if success:
            # Mark step as completed
            user.add_completed_step(user.current_step)
            
            # Move to next step if not the last one
            if user.current_step < 13:
                user.current_step += 1
            
            # Update last active
            user.last_active = datetime.datetime.utcnow()
            
            db.session.commit()
            
            # Get next step info
            next_step = None
            if user.current_step <= 13:
                next_step_obj = ScavengerStep.query.get(user.current_step)
                if next_step_obj:
                    next_step = next_step_obj.to_dict_for_user()
            
            return jsonify({
                'success': True,
                'message': 'Correct! Moving to next clue.',
                'next_step': next_step,
                'completed_hunt': user.current_step > 13
            }), 200
        else:
            db.session.commit()
            return jsonify({
                'success': False,
                'message': 'Wrong location – try again!'
            }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hunt_bp.route('/reveal-location', methods=['POST'])
@require_auth
def reveal_location(user):
    try:
        # Add current step to revealed locations
        user.add_revealed_location(user.current_step)
        user.last_active = datetime.datetime.utcnow()
        db.session.commit()
        
        # Get current step with location revealed
        current_step = ScavengerStep.query.get(user.current_step)
        if not current_step:
            return jsonify({'error': 'Step not found'}), 404
        
        return jsonify({
            'revealed': True,
            'location': current_step.name,
            'message': f'Location revealed: {current_step.name}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hunt_bp.route('/progress', methods=['GET'])
@require_auth
def get_progress(user):
    try:
        completed_steps = user.get_completed_steps()
        revealed_locations = user.get_revealed_locations()
        
        # Get all steps for progress display
        all_steps = ScavengerStep.query.order_by(ScavengerStep.id).all()
        steps_info = []
        
        for step in all_steps:
            step_info = {
                'id': step.id,
                'name': step.name,
                'completed': step.id in completed_steps,
                'revealed': step.id in revealed_locations,
                'current': step.id == user.current_step
            }
            
            # Only show clue for current step or completed steps
            if step.id == user.current_step or step.id in completed_steps:
                step_info['clue'] = step.clue
            
            steps_info.append(step_info)
        
        return jsonify({
            'current_step': user.current_step,
            'total_steps': 13,
            'completed_count': len(completed_steps),
            'steps': steps_info,
            'completed_hunt': len(completed_steps) >= 13
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

