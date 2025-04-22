from flask import Blueprint,url_for, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
import json
index_views = Blueprint('index_views', __name__, template_folder='../templates')
from App.models import Listing, User, Amenity, Images, db
from flask_jwt_extended import jwt_required, unset_jwt_cookies, set_access_cookies, create_access_token, get_jwt_identity

def get_current_user():
    #helper function for getting user
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        print("in current user function")
        user_id = get_jwt_identity()
        print(f"This is get_jwt_identity: {user_id}")
        print("\nafter current user function")
        if user_id:
            return User.query.filter_by(id=user_id).first()
    except Exception:
        print("Fails at get_jwt_identity")
        pass
    return None


def initializedb():

    initialize()
    bob = create_user('bob', 'bobpass', 'bob@mail.com')
    alice = create_user('alice', 'alicepass', 'alice@mail.com')
    charlie = create_user('charlie', 'charliepass', 'charlie@mail.com')

    db.session.add(bob)
    db.session.add(alice)
    db.session.add(charlie)
    db.session.commit()
    #set up database
    with open('App/static/apartment_listings.json') as f:
        listings = json.load(f)
        for l in listings:
            landlord_id = l['landlord_id']
            city = l['city']
            address = l['address']
            price = l['price']
            bedrooms = l['bedrooms']
            bathrooms = l['bathrooms']
            amenities = l['amenities']
            carouselPhotos = l['carouselPhotos']

            new_listing = Listing(
                address=address,
                city=city,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                landlord_id=landlord_id
            )
            db.session.add(new_listing)
            db.session.commit()
            print(f"This is the listing id: {new_listing.id}")
            new_amenity = Amenity(
                apartment_id=new_listing.id,
                wifi=False,
                air_conditioning=False,
                kitchen=False,
                parking=False,
                laundry=False,
                pool=False,
                tv=False
            )
            for amenity in amenities:
                if amenity == 'WiFi':
                    new_amenity.wifi = True
                    print(f'Has WIFI')
                if amenity == 'AC':
                    print(f'Has AC')
                    new_amenity.air_conditioning = True
                if amenity == 'Kitchen':
                    print(f'Has Kitchen')
                    new_amenity.kitchen = True
                if amenity == 'Parking':
                    print(f'Has Parking')
                    new_amenity.parking = True
                if amenity == 'Laundry':
                    print(f'Has Laundry')
                    new_amenity.laundry = True
                if amenity == 'Pool':
                    print(f'Has Pool')
                    new_amenity.pool = True
                if amenity == 'TV':
                    print(f'Has TV')
                    new_amenity.tv = True

            print(f'\n\n')

            db.session.add(new_amenity)
            for image in carouselPhotos:
                new_image = Images(
                    image_url=image['url'],
                    apartment_id=new_listing.id
                )
                db.session.add(new_image)
        db.session.commit()
                
    
@index_views.route('/init', methods=['GET'])
def init():
    initializedb()
    data = User.query.all()
    return jsonify({
        'status': 'success',
        'message': 'Database initialized successfully',
        'data': [user.to_dict() for user in data]
    })

@index_views.route('/', methods=['GET'])
def landing_page():
    return render_template('landing.html', user=get_current_user())

@index_views.route('/listing', methods=['GET'])
@jwt_required()
def home_page():
    current_user = get_current_user()

    if not current_user:
        return redirect(url_for('auth_views.login'))

    listings = Listing.query.all()
    if not listings:
        return jsonify({'status': 'error', 'message': 'No listings found'}), 404
    for listing in listings:
        print(f"{listing.images[0].image_url}\n")
    return render_template('listings.html', apartments=listings, user=get_current_user())


@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
