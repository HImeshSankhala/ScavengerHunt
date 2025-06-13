from src.models.database import db

class ScavengerStep(db.Model):
    __tablename__ = 'scavenger_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    clue = db.Column(db.Text, nullable=False)
    qr_code_url = db.Column(db.String(500), nullable=True)
    qr_code_value = db.Column(db.String(255), nullable=False, unique=True)
    
    # Relationships
    scan_events = db.relationship('ScanEvent', backref='step', lazy=True)
    
    def __init__(self, id, name, clue, qr_code_url, qr_code_value):
        self.id = id
        self.name = name
        self.clue = clue
        self.qr_code_url = qr_code_url
        self.qr_code_value = qr_code_value
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'clue': self.clue,
            'qr_code_url': self.qr_code_url,
            'qr_code_value': self.qr_code_value
        }
    
    def to_dict_for_user(self):
        # Return version without QR code value for security
        return {
            'id': self.id,
            'name': self.name,
            'clue': self.clue,
            'qr_code_url': self.qr_code_url
        }

