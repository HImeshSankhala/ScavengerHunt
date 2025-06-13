import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.database import db
from src.routes.auth import auth_bp
from src.routes.hunt import hunt_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'scavenger-hunt-secret-key-2024'

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(hunt_bp, url_prefix='/api/hunt')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Import and register user blueprint for health check
from src.routes.user import user_bp
app.register_blueprint(user_bp, url_prefix='/api')

# Database configuration - using SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scavenger_hunt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    # Initialize default data
    from src.models.scavenger_step import ScavengerStep
    from src.models.admin_user import AdminUser
    from werkzeug.security import generate_password_hash
    
    # Create default admin user if not exists
    if not AdminUser.query.filter_by(username='admin').first():
        admin = AdminUser(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
    
    # Create scavenger hunt steps if not exist
    if ScavengerStep.query.count() == 0:
        steps_data = [
            {
                "id": 1,
                "name": "Black Cat Alley",
                "clue": "Find the place where cats don't purr — they pop with color on the wall for sure.",
                "qr_code_url": "URL_TO_QR_CODE_1",
                "qr_code_value": "BLACKCAT_ALLEY_001"
            },
            {
                "id": 2,
                "name": "Milwaukee Art Museum",
                "clue": "What flaps like a bird but never flies? Find the building that spreads its wings by the lake.",
                "qr_code_url": "URL_TO_QR_CODE_2",
                "qr_code_value": "ART_MUSEUM_002"
            },
            {
                "id": 3,
                "name": "Discovery World",
                "clue": "Where science meets the sea, you'll find a big ship and tech to see.",
                "qr_code_url": "URL_TO_QR_CODE_3",
                "qr_code_value": "DISCOVERY_WORLD_003"
            },
            {
                "id": 4,
                "name": "Lakeshore State Park",
                "clue": "A park on water — now that's rare! Find the trail with skyline flair.",
                "qr_code_url": "URL_TO_QR_CODE_4",
                "qr_code_value": "LAKESHORE_PARK_004"
            },
            {
                "id": 5,
                "name": "Pierhead Lighthouse",
                "clue": "It's red and bright and guards the shore, you'll find it near the lakeside floor.",
                "qr_code_url": "URL_TO_QR_CODE_5",
                "qr_code_value": "PIERHEAD_LIGHT_005"
            },
            {
                "id": 6,
                "name": "Historic Third Ward",
                "clue": "Old warehouses with modern flair, boutiques and murals everywhere!",
                "qr_code_url": "URL_TO_QR_CODE_6",
                "qr_code_value": "THIRD_WARD_006"
            },
            {
                "id": 7,
                "name": "The Hop - Historic Third Ward Stop",
                "clue": "You don't need a ticket, just wait for the ride. Find the streetcar track and pose with pride!",
                "qr_code_url": "URL_TO_QR_CODE_7",
                "qr_code_value": "HOP_STATION_007"
            },
            {
                "id": 8,
                "name": "Milwaukee Public Market",
                "clue": "Inside this market, smells float in the air — find cheese, spice, or chocolate fair!",
                "qr_code_url": "URL_TO_QR_CODE_8",
                "qr_code_value": "PUBLIC_MARKET_008"
            },
            {
                "id": 9,
                "name": "Gertie the Duck Statue",
                "clue": "She once sat beneath a bridge, a wartime hero with a nest to rig.",
                "qr_code_url": "URL_TO_QR_CODE_9",
                "qr_code_value": "GERTIE_DUCK_009"
            },
            {
                "id": 10,
                "name": "The Bronze Fonz",
                "clue": '"Ayyyy!" is what he\'d say — find this cool guy by the river today.',
                "qr_code_url": "URL_TO_QR_CODE_10",
                "qr_code_value": "BRONZE_FONZ_010"
            },
            {
                "id": 11,
                "name": "Marcus Performing Arts Center",
                "clue": "Music and drama live here night and day. Find a poster or sculpture on display!",
                "qr_code_url": "URL_TO_QR_CODE_11",
                "qr_code_value": "MARCUS_ARTS_011"
            },
            {
                "id": 12,
                "name": "Milwaukee City Hall",
                "clue": "With its tall clock tower and historic face, this building stands with elegant grace.",
                "qr_code_url": "URL_TO_QR_CODE_12",
                "qr_code_value": "CITY_HALL_012"
            },
            {
                "id": 13,
                "name": "The Pfister Hotel / Blu Lounge",
                "clue": "Time to celebrate your final clue — find the place with a stunning view.",
                "qr_code_url": "URL_TO_QR_CODE_13",
                "qr_code_value": "PFISTER_HOTEL_013"
            }
        ]
        
        for step_data in steps_data:
            step = ScavengerStep(**step_data)
            db.session.add(step)
    
    db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
