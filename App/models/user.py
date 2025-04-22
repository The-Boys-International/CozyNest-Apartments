from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime
from App.database import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_landlord = db.Column(db.Boolean, default=False)
    is_tenant = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    listings = db.relationship('Listing', backref='landlord', lazy=True)
    reviews = db.relationship('Review', backref='tenant', lazy=True)
    
    
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password, method='sha256')

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }
        
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_landlord': self.is_landlord,
            'is_tenant': self.is_tenant,
            'created_at': self.created_at.isoformat(),
            'listings': [ listing.to_dict() for listing in self.listings ]
        }
        
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)
