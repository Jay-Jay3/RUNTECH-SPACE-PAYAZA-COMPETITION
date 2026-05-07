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
    method = data.get('method')
    escrow_id = data.get('escrow_id')
    # fetch escrow details from DB
    escrow = Escrow.query.get(escrow_id)
    if not escrow:
        return jsonify({
            "error": "Escrow not found"
        }), 400
    
    tx_ref = f"ESC_{escrow.id}_{uuid.uuid7().hex[:4]}"

    if method == 'card':
        # creating the payaza payload
        # Note this is not getting amount from frontend because it is not reliable and secure
        card_payload = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email_address": data['email'],
            "phone_number": data['phone_number'],
            "amount": float(escrow.amount),
            "transaction_reference": f"ESC-{escrow_id}-{uuid.uuid7().hex[:6]}",
            "currency": "NGN",
            "description": "Test",
            "card": data['card'],  #either expiry, cvv, number 
            "callback_url": "https://runtech-space-payaza-competition.onrender.com/docs"
        }

        # Calling payaza from the transaction file
        response = pay_Aza.card_charge(card_payload)

    elif method == 'momo':
        momo_payload = {
            "amount": data['amount'],
            "customer_number": data['customer_phone'],
            "transaction_reference": data['trans_ref'],
            "transaction_description": data['trans_desc'],
            "customer_bank_code": data['bank_code'],
            "currency_code": data['currency'],
            "customer_email": data['email'],
            "customer_first_name": data['first_name'],
            "customer_last_name": data['last_name'],
            "customer_phone_number": data['customer_phone'],
            "country_code": data['country']
        }

        response = pay_Aza.momo_collection(momo_payload)

    elif method == 'va':
        va_payload = {

        }

        response = pay_Aza.create_virtual_account(va_payload)

    elif method == 'transfer':
        merchant_info = pay_Aza.get_merchant_details()
        return jsonify({
            "Status": "manual action required",
            "instructions": "Transfer to the account below and use a specific reference that tells the name of the product and the name of the business",
            "bank details": merchant_info.get('data'),
            "reference to use": tx_ref
        })

    # saving to the sql table
    new_tx = Transaction(
        escrow_id=escrow.id,
        reference=card_payload['transaction_reference'],
        amount=escrow.amount,
        currency=card_payload['currency'],
        raw_response=response,
        method=method
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


# Manual checking from the user
@payaza.route("verify-payment/<transaction_ref>", methods=['GET'])
def verify_payment(transaction_ref):
    tx = Transaction.query.filter_by(reference=transaction_ref).first_or_404()

    if tx.method == 'card':
        response = pay_Aza.check_card_status(transaction_ref)
    elif tx.method == 'momo':
        response = pay_Aza.check_momo_transaction_status(transaction_ref)
    elif tx.method == 'va':
        response = pay_Aza.get_transfer_status(transaction_ref)
    else:
        return jsonify({
            "message": "Wrong endpoint"
        })
        
    
    if response.get('status') == "Completed" or response.get('data', {}).get('status') == 'Successful'or response.get('data', {}).get('status') == 'SUCCESSFUL':
        tx.status = "SUCCESSFUL"
        tx.escrow.status = "FUNDED"
        db.session.commit()
        return jsonify({
            "message": "Payment verified! Escrow is now funded"
        })
    return jsonify({
        "message": "Payment not yet confirmed",
        "details": response
    }), 200



# The automatic webhook that PAYAZA SHOULD GIVE US
@payaza.route("/payaza-webhook", methods=['POST'])
def payaza_webhook():
    payload = request.json
    
    # verification of Payaza header to ensure there is no fraud or hacking

    tx_ref = payload.get("transaction_reference") or payload.get('data',{}).get('transaction_reference')

    tx = Transaction.query.filter_by(reference=tx_ref).first()
    if tx and tx.status != "SUCCESSFUL":
        received_amount = payload.get('amount') or payload.get('data', {}).get('amount')
        if tx.amount >=  received_amount :
            tx.status = "SUCCESSFUL"
            tx.escrow.status = 'FUNDED'
            db.session.commit()

    return jsonify({"status", "acknowledged"}), 200




