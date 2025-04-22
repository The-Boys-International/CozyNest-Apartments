from App.database import db

class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable = False)
    image_url = db.Column(db.String(500), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Amenity {self.name}>'