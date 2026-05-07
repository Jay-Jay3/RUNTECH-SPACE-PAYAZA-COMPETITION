from flask import request, jsonify
from flask_smorest import Blueprint
from app.modal import db, Transaction, Escrow, User, Vendor
from flask_login import login_user, logout_user, login_required, current_user
from app.services.Payaza_service import PayazaServices
from app.services.user_svc import UserServices
from app.routes import unified_data
from app.routes.payout import is_verify_seller_bank
import uuid_utils as uuid

payaza = Blueprint("user", __name__, "This is for all routes that lead to the user functionality")
pay_Aza = PayazaServices()

userService = UserServices()

@payaza.route('/api/register', methods=['POST'])
@unified_data
def register(data):
    # data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not password:
        return jsonify({"error": "Missing credentials"}), 408

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409
    

    user = userService.create_user(data)

    return jsonify({
        "message": "User created successfully",
        "id": user.id,
        "email": user.email,
        "name": user.name
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

@payaza.route('/api/register/vendor', methods=['POST'])
@unified_data
def register_vendor(data):
    detail = {data['account_number'], data['bank_code']}
    if not is_verify_seller_bank(detail):
        return jsonify({
            "error": "Can not create business, Invalid bank details",
            "message": "Input valid bank account"
        })
    vendor = Vendor.query.filter(
        (Vendor.business_name == data['business_name']) | 
        (Vendor.business_email == data['business_email'])
    ).first()
    if vendor:
        return jsonify({
            "error": "This data exists",
            "message": "This data exists: your business name and email"
        })

