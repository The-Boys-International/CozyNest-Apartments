from App.database import db

class Amenity(db.Model):

    __tablename__ = 'amenity'
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable = False, unique=True)
    wifi = db.Column(db.Boolean, default=False)
    air_conditioning = db.Column(db.Boolean, default=False)
    kitchen = db.Column(db.Boolean, default=False)
    parking = db.Column(db.Boolean, default=False)
    laundry = db.Column(db.Boolean, default=False)
    pool = db.Column(db.Boolean, default=False)
    tv = db.Column(db.Boolean, default=False)
    listing = db.relationship('Listing', back_populates='amenities')
    
    def __init__(self, apartment_id, wifi=False, air_conditioning=False, kitchen=False,
                 parking=False, laundry=False, pool=False, tv=False):
        self.apartment_id = apartment_id
        self.wifi = wifi
        self.air_conditioning = air_conditioning
        self.kitchen = kitchen
        self.parking = parking
        self.laundry = laundry
        self.pool = pool
        self.tv = tv


    def __repr__(self):
        return f'<Amenity {self.name}>'