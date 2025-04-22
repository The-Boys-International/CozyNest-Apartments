from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, create_access_token
#from flask_login import login_user, logout_user, current_user, login_required


from App.models import db
from App.models import User
from App.models import *

from.index import index_views

from App.controllers import (
    login,
    create_user
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

def get_current_user():
    #helper function to get current user
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

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            response = redirect(url_for('index_views.home_page'))
            set_access_cookies(response, access_token)
            flash(f'Login successful! with user name {user.username} and id{user.id}.', 'success')
            return response
        else:
            return render_template('login.html', user = None, message="Invalid credentials")
    return render_template('login.html', user = None, message="")

@auth_views.route('/logout', methods=['GET'])
def logout():
    response = redirect(url_for('index_views.landing_page'))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data_username = request.form['username']
        data_email = request.form['email']
        data_password = request.form['password']
        
        #1 check if email already exists
        email = User.query.filter_by(email=data_email).first()
        if email:
            flash('Email already exists!', 'error')
            return render_template('signup.html', message="Email already exists!", user=get_current_user())
        #1

        #2 check if username already exists
        username = User.query.filter_by(username=data_username).first()
        if username:
            flash('Username already exists!', 'error')
            return render_template('signup.html', message="Username already exists!", user=get_current_user())
        #2

        #create a new user

        new_user = create_user(username=data_username, password=data_password, email=data_email)
        
        #create JWT token and set cookies
        access_token = create_access_token(identity=str(new_user.id))
        response = redirect(url_for('index_views.home_page', user = new_user))
        set_access_cookies(response, access_token)
        flash("Sign up successful! Welcome aboard.", "success")
        return response
        
    
    return render_template('signup.html', message = "", user=get_current_user())

if __name__ == '__main__':
    app.run(debug=True)

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response