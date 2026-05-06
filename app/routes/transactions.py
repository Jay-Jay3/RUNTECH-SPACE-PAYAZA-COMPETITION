from flask import request, jsonify
from flask_smorest import Blueprint
from app.modal import db, Transaction, Escrow
from app.services.Payaza_service import PayazaServices
from app.routes import unified_data
import uuid_utils as uuid

payaza = Blueprint("payment", __name__, "This is for all routes that lead to the webapi")
pay_Aza = PayazaServices()

@payaza.route("/initiate-card-payment", methods=["POST"])
@unified_data
def initiate_payment(data):
    escrow_id = data.get('escrow_id')
    # fetch escrow details from DB
    escrow = Escrow.query.get(escrow_id)
    if not escrow:
        return jsonify({
            "error": "Escrow not found"
        }), 400
    
    # creating the payaza payload
    # Note this is not getting amount from frontend because it is not reliable and secure
    card_payload = {
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "email_address": data['email'],
        "amount": float(escrow.amount),
        "transaction_reference": f"ESC-{escrow_id}-{uuid.uuid7().hex[:6]}",
        "currency": "NGN",
        "card": data['card']  #either expiry, cvv, number 
    }

    # Calling payaza from the transaction file
    response = pay_Aza.card_charge(card_payload)

    # saving to the sql table
    new_tx = Transaction(
        escrow_id=escrow.id,
        reference=card_payload['transaction_reference'],
        amount=escrow.amount,
        currency=card_payload['currency'],
        raw_response=response
    )
    db.session.add(new_tx)
    db.session.commit()

    return jsonify(response)


@payaza.route("/pay-into-vault", methods=["POST"])
@unified_data
def pay_into_wallet(data):
    escrow_id = data.get('escrow_id')
    # fetch escrow details from DB
    escrow = Escrow.query.get(escrow_id)

    # I tries to tag the payment using the escrow_id
    tx_ref = f"ESCROW_HOLD_{escrow_id}"

    # NOTe INSIDE HERE IS WHERE YOU WILL REMOVE THE VHARGES AND THE FEE
    """"""

    new_tx = Transaction(
        escrow_id = escrow_id,
        reference=tx_ref,
        status="awaiting_confirmation",
        amount= escrow.amount,
        currency = escrow.currency
    )
    db.session.add(new_tx)
    db.session.commit()
    
    return jsonify({
        "message": "Payment initialised",
        "reference": tx_ref
    })




