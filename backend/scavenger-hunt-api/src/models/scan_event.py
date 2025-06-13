import uuid
from datetime import datetime
from src.models.database import db

class ScanEvent(db.Model):
    __tablename__ = 'scan_events'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('scavenger_steps.id'), nullable=False)
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, nullable=False)
    revealed_first = db.Column(db.Boolean, default=False)
    
    def __init__(self, user_id, step_id, success, revealed_first=False):
        self.user_id = user_id
        self.step_id = step_id
        self.success = success
        self.revealed_first = revealed_first
        self.scanned_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'step_id': self.step_id,
            'scanned_at': self.scanned_at.isoformat(),
            'success': self.success,
            'revealed_first': self.revealed_first
        }

