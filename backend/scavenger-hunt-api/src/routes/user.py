from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'scavenger-hunt-api'}), 200

