from flask import request, jsonify
from flask_smorest import Blueprint
from app.modal import db, Transaction, Escrow
from app.services.Payaza_service import PayazaServices
from app.routes import unified_data
import uuid_utils as uuid

payaza = Blueprint("user", __name__, "This is for all routes that lead to the webapi")
pay_Aza = PayazaServices()

@payaza.route("/user/initiate-card-payment", methods=["POST"])
@unified_data
def initiate_payment(data):
    return