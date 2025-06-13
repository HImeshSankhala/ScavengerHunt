from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from src.models.database import db
from src.models.user import User
from src.models.admin_user import AdminUser
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

# Secret key for JWT (in production, use environment variable)
JWT_SECRET = 'scavenger-hunt-jwt-secret-2024'

def generate_token(user_id, is_admin=False):
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        phone = data.get('phone')
        
        if not email and not phone:
            return jsonify({'error': 'Email or phone number required'}), 400
        
        # Find or create user
        user = None
        if email:
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email)
                db.session.add(user)
                db.session.commit()
        elif phone:
            user = User.query.filter_by(phone=phone).first()
            if not user:
                user = User(phone=phone)
                db.session.add(user)
                db.session.commit()
        
        # Update last active
        user.last_active = datetime.datetime.utcnow()
        db.session.commit()
        
        # Generate token
        token = generate_token(user.id)
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Find admin user
        admin = AdminUser.query.filter_by(username=username).first()
        if not admin or not check_password_hash(admin.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate admin token
        token = generate_token(admin.id, is_admin=True)
        
        return jsonify({
            'token': token,
            'admin': admin.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid token'}), 401
        
        if payload.get('is_admin'):
            admin = AdminUser.query.get(payload['user_id'])
            if not admin:
                return jsonify({'error': 'Admin not found'}), 404
            return jsonify({'admin': admin.to_dict()}), 200
        else:
            user = User.query.get(payload['user_id'])
            if not user:
                return jsonify({'error': 'User not found'}), 404
            return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # For JWT, logout is handled client-side by removing the token
    return jsonify({'message': 'Logged out successfully'}), 200

