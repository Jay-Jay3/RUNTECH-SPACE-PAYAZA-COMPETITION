import requests
import os
import base64
from dotenv import load_dotenv
from app import db
from app.modal import User, Vendor 

load_dotenv()

class UserServices:
    def __init__(self):
        self.table = "users"
    
    def create_user(self, details):
        user = User.query.filter_by(email=details['email']).first()
        if user:
            return {"error": "User already exists"}
        
        new_user = User(   
                    name=details['name'],
                    email=details['email'],
                    phone=details['phone'],
                    address=details['address'],
                    is_vendor=details['is_vendor'],
        )
        new_user.set_password(details['password'])
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    def update_records(self, id, data):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}
        
        allowed_fields = {'name','phone', 'address', 'is_vendor'}
        
        
        for key, value in data.items():
            if key in allowed_fields:
                setattr(user, key, value)

        db.session.commit()

        return {"message": "Change effected"}
    
    def delete_user(self, id):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}
        db.session.delete(user)
        db.session.commit()
        return {
            "message": "User deleted successfully",
            "user": user
        }
    
    def find_user(self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}
        return user
    
    def create_vendor(self, details):
        user = User.query.filter_by(email=details['email'])
        if not user:
            return {"error": "User does not exists"}
        
        new_user = Vendor(   
                    business_name=details['business_name'],
                    business_email=details['business_email'],
                    business_address=details['business_address'],
                    business_phone=details['business_phone'],
                    account_number=details['business_number'],
                    account_name=details['account_name'],
                    bank_code=details['bank_code'],
                    user_id=user.id
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    def update_vendor_records(self, id, value):
        vendor = Vendor.query.get(id)
        allowed_fields = {
            'business_name', 
            'business_address', 
            'business_phone', 
            'account_name', 
            'account_number', 
            'bank_code'}
        
        
        for key, value in value.items():
            if key in allowed_fields:
                setattr(vendor, key, value)
            
        db.session.commit()
        return {
            "message": "The vendor's profile has ben pdated succesffulyy",
            "vendor": vendor
            }

