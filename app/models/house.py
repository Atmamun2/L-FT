from datetime import datetime
from app import db

class House(db.Model):
    __tablename__ = 'houses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    founder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    motto = db.Column(db.String(200))
    rules = db.Column(db.Text)
    last_merge_date = db.Column(db.DateTime)
    
    # Relationships
    members = db.relationship('User', backref='house', lazy=True)
    transactions = db.relationship('Transaction', backref='house', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'member_count': len(self.members),
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
            'motto': self.motto
        }
    
    def __repr__(self):
        return f'<House {self.name}>'
