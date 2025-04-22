from flask import Blueprint, current_app, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, get_jwt_identity
from werkzeug.utils import secure_filename
from sqlalchemy import func
import os
from.index import index_views
from App.models import db, Listing, Amenity, Images, User, Review
import random
import string
from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
)

def random_string():
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

extensions = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
  if '.' in filename:
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in extensions
  return False

user_views = Blueprint('user_views', __name__, template_folder='../templates')

def allowed_file(filename):
    return ('.' in filename
            and filename.rsplit('.', 1)[1].lower()
            in extensions)

def get_current_user():
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

@user_views.route('/create-listing', methods=['GET', 'POST'])
def create_listing():
    current_user = get_current_user()
    print(f"Current user: {current_user}")
    if request.method == 'POST':

        address = request.form['address']
        city = request.form.get('city', '')
        price = float(request.form['price'])
        bedrooms = int(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])

        listing = Listing(
            address=address,
            city=city,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            landlord_id=current_user.id
        )
        db.session.add(listing)
        db.session.flush()


        picked = request.form.getlist('amenities')
        amenity = Amenity(
            apartment_id=listing.id,
            wifi='WiFi' in picked,
            air_conditioning='Air Conditioning' in picked,
            kitchen='Kitchen' in picked,
            parking='Parking' in picked,
            laundry='Laundry' in picked,
            pool='Pool' in picked,
            tv=False
        )
        db.session.add(amenity)

        files = request.files.getlist('images')
        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                filename = random_string() + '_' + filename
                save_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    filename
                )
                f.save(save_path)

                url = url_for(
                    'static',
                    filename='uploads/' + filename,
                    _external=False
                )
                img = Images(
                    apartment_id=listing.id,
                    image_url=url
                )
                db.session.add(img)

        db.session.commit()
        return redirect(url_for('index_views.home_page'))

    return render_template('createlistings.html', user = get_current_user())

@user_views.route('/details/<int:listing_id>', methods=['GET','POST'])
def view_details(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    current_user= get_current_user()
    print(f"This is outside POST") #debugging
    if request.method == 'POST':
        print(f"This is inside POST") #debugging
        rating  = int(request.form.get('rating', 0))
        comment = request.form.get('comment', '').strip()

        print(f"Rating: {rating}\n")#debugging
        print(f"Comment: {comment}")#debugging

        if not (1 <= rating <= 5):
            flash('Invalid rating.', 'danger')
            return redirect(url_for('user_views.view_details', user = get_current_user(), listing_id=listing_id, reviews=listing.reviews))

        review = Review(
            rating=rating,
            comment=comment,
            apartment_id=listing_id,
            user_id=current_user.id,
            username=current_user.username
        )
        db.session.add(review)
        db.session.commit()
        
        reviews = Review.query.filter_by(apartment_id=listing_id).all()

        counter = 0
        total = 0
        for r in reviews:     #getting average
            counter+=1 
            total+= r.rating
        if counter > 0:
            avg = total / counter
        else:
            avg = 0
        
        listing = Listing.query.get_or_404(listing_id)
        listing.avg_rating = (int)(round(float(avg), 2))
        db.session.commit()

        flash('Thank you! Your review has been submitted.', 'success')
        return redirect(url_for('user_views.view_details', user = get_current_user(), listing_id=listing_id, reviews=listing.reviews))
    return render_template('details.html', user = get_current_user(), property=listing, reviews=listing.reviews)

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')