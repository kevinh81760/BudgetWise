from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from server.database import Session
from server.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    session_db = Session()
    existing_user = session_db.query(User).filter_by(username=username).first()

    if existing_user:
        session_db.close()
        return jsonify({"error": "Username already exists."}), 409

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    new_user = User(username=username, password=hashed_password)
    session_db.add(new_user)
    session_db.commit()
    session_db.close()

    return jsonify({"message": "User registered successfully!"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    session_db = Session()
    user = session_db.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session_db.close()
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        session_db.close()
        return jsonify({"error": "Invalid username or password"}), 401