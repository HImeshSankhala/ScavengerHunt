import uuid
from datetime import datetime
from src.models.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    current_step = db.Column(db.Integer, default=1)
    completed_steps = db.Column(db.Text, default='[]')  # JSON array as string
    revealed_locations = db.Column(db.Text, default='[]')  # JSON array as string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    scan_events = db.relationship('ScanEvent', backref='user', lazy=True)
    
    def __init__(self, email=None, phone=None):
        self.email = email
        self.phone = phone
        self.current_step = 1
        self.completed_steps = '[]'
        self.revealed_locations = '[]'
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'current_step': self.current_step,
            'completed_steps': json.loads(self.completed_steps),
            'revealed_locations': json.loads(self.revealed_locations),
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat()
        }
    
    def add_completed_step(self, step_id):
        import json
        completed = json.loads(self.completed_steps)
        if step_id not in completed:
            completed.append(step_id)
            self.completed_steps = json.dumps(completed)
    
    def add_revealed_location(self, step_id):
        import json
        revealed = json.loads(self.revealed_locations)
        if step_id not in revealed:
            revealed.append(step_id)
            self.revealed_locations = json.dumps(revealed)
    
    def get_completed_steps(self):
        import json
        return json.loads(self.completed_steps)
    
    def get_revealed_locations(self):
        import json
        return json.loads(self.revealed_locations)

