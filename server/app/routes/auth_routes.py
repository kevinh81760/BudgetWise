from flask import Blueprint, request, session
from database import Session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    session_db = Session()

    username = request.form['username']
    password = request.form['password']

    existingUser = session_db.query(User).filter_by(username=username).first()
    if(existingUser):
        session_db.close
        return "Username already exists. Choose a different one.", 400
    
    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password=hashed_password)
    session_db.add(new_user)
    session_db.commit()
    session_db.close()

    return "User registered successfully!", 201

@auth.route('/login', methods=['POST'])
def login():
    session_db = Session()

    username = request.form['username']
    password = request.form['password']

    user = session_db.query(User).filter_by(username=username).first()

    # checks if user exist and checks if the user password  matches with password field
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return "Successfully logged in!"
    else:
        return "Invalid username or password"


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return "Logged out successfully!"
