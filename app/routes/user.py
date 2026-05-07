from flask import request, jsonify
from flask_smorest import Blueprint
from app.modal import db, Transaction, Escrow, User
from flask_login import login_user, logout_user, login_required, current_user
from app.services.Payaza_service import PayazaServices
from app.services.user_svc import UserServices
from app.routes import unified_data
import uuid_utils as uuid

payaza = Blueprint("user", __name__, "This is for all routes that lead to the user functionality")
pay_Aza = PayazaServices()

userService = UserServices()

@payaza.route('/api/register', methods=['POST'])
@unified_data
def register(data):
    # data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 409

    use = userService.create_user(data)

    return jsonify({
        "message": "User created successfully",
        "user": use
        }), 201

@payaza.route('/api/login', methods=['POST'])
@unified_data
def login(data):
#     # data = request.get_json()

    user = userService.find_user(data['email'])
    if user and user.check_password(data.get('password')):
        login_user(user)
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@payaza.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@payaza.route('/api/protected')
@login_required
def protected():
    return jsonify({
        "message": "You are in the protected area",
        "user": current_user.to_dict()
    })
