from App.database import db
from datetime import datetime

class Review(db.Model):
    """Review model for apartment ratings"""
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(5000), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    apartment_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(64), nullable=False)

    def __init__(self, rating, comment, apartment_id, user_id, username):
        self.rating = rating
        self.comment = comment
        self.apartment_id = apartment_id
        self.user_id = user_id
        self.username = username

    def __repr__(self):
        return f'<Review {self.rating} stars for Apartment {self.apartment_id}>'
