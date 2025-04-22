from App.database import db
from datetime import datetime

from .amenity import *

class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    
    avg_rating = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    images = db.relationship('Images', backref='listing', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='listing', lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', back_populates='listing', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Apartment {self.address}, {self.city}>'

    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'city': self.city,
            'price': self.price,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'created_at': self.created_at.isoformat(),
            'landlord_id': self.landlord_id,
            'images': [ img.image_url for img in self.images ],
            'amenities': {

                'wifi': self.amenities.wifi if self.amenities else False,
                'air_conditioning': self.amenities.air_conditioning if self.amenities else False,
                'kitchen': self.amenities.kitchen if self.amenities else False,
                'parking': self.amenities.parking if self.amenities else False,
                'laundry': self.amenities.laundry if self.amenities else False,
                'pool': self.amenities.pool if self.amenities else False,
                'tv': self.amenities.tv if self.amenities else False,
            }
        }