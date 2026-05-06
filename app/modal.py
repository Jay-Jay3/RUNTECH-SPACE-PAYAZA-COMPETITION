from app import db
from datetime import datetime
from uuid_utils import uuid7

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, nullable=False, primary_key=True, default=lambda:str(uuid7()), unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)

    is_vendor = db.Column(db.Boolean, default=False)


class Vendor(db.Model):
    __tablename__ = "vendors"

    id = db.Column(db.String, nullable=False, primary_key=True, default=lambda:str(uuid7()), unique=True)

    business_name = db.Column(db.String, nullable=False)
    business_email = db.Column(db.String, nullable=False, unique=True)
    business_address = db.Column(db.String, nullable=False)
    business_phone = db.Column(db.String, nullable=False)

    account_number = db.Column(db.String, nullable=False)
    account_name = db.Column(db.String, nullable=False)
    bank_code = db.Column(db.String, nullable=False)

    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Numeric(3, 2), nullable=True)


class Escrow(db.Model):
    __tablename__ = "escrows"

    id = db.Column(db.String, nullable=False, primary_key=True, default=lambda:str(uuid7()), unique=True)
    buyer_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.String, db.ForeignKey('vendors.id'), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="pending")
    payment_reference = db.Column(db.String, nullable=True)
    statements = db.relationship('ContractStatement', backref='escrow', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.String, nullable=False, primary_key=True, default=lambda:str(uuid7()), unique=True)
    escrow_id = db.Column(db.String, db.ForeignKey("escrows.id"), nullable=False)
    gateway  = db.Column(db.String, default="payaza")
    reference = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String,default="pending")
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String, nullable=False)
    raw_response = db.Column(db.JSON)

class Payout(db.Model):
    __tablename__ = "payouts"

    id = db.Column(db.String, nullable=False, primary_key=True, default=lambda:str(uuid7()), unique=True)
    escrow_id = db.Column(db.String, db.ForeignKey("escrows.id"), nullable=False)
    seller_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="pending")
    reference = db.Column(db.String, nullable=False)

class Dispute(db.Model):
    __tablename__ = "dispute"

    id = db.Column(db.String, nullable=False, primary_key=True, default=lambda:str(uuid7()), unique=True)
    escrow_id = db.Column(db.String, db.ForeignKey("escrows.id"), nullable=False)
    opened_by = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default="open")
    resolution = db.Column(db.Text, nullable=True)

class ContractStatement(db.Model):
    __tablename__ = "contract_statements"

    id = db.Column(db.String, nullable=False, primary_key=True, default=lambda:str(uuid7()), unique=True)
    escrow_id = db.Column(db.String, db.ForeignKey('escrows.id'), nullable=False)
    statement_text = db.Column(db.Text, nullable=False)
    is_fulfilled = db.Column(db.Boolean, default=False)
    fulfilled_at = db.Column(db.DateTime, nullable=True)

    required_confirmation_from = db.Column(db.String, default='buyer')




# class 

