from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from server.database import Session
from server.models.user import User

# Blueprint for handling authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """
    Registers a new user by creating a new User record in the database.

    Request JSON:
        {
            "username": "<string>",
            "password": "<string>"
        }

    Returns:
        JSON response with success or error message and HTTP status code.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate presence of both username and password
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    session_db = Session()
    
    # Check if the username exists already
    existing_user = session_db.query(User).filter_by(username=username).first()

    if existing_user:
        session_db.close()
        return jsonify({"error": "Username already exists."}), 409

    # Hash the password securely
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    new_user = User(username=username, password=hashed_password) # Add new user to the database
    session_db.add(new_user)
    session_db.commit()
    session_db.close()

    return jsonify({"message": "User registered successfully!"}), 201

@auth.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user by checking the provided credentials.

    Request JSON:
        {
            "username": "<string>",
            "password": "<string>"
        }

    Returns:
        JSON response with success or error message and HTTP status code.
    """
    data = request.get_json()
    username = data['username']
    password = data['password']

    session_db = Session()
    
    # Retrieve the user record by username
    user = session_db.query(User).filter_by(username=username).first()

    # Validate password using hashed comparison
    if user and check_password_hash(user.password, password):
        session_db.close()
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        session_db.close()
        return jsonify({"error": "Invalid username or password"}), 401