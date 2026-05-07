from flask import request, jsonify
from flask_smorest import Blueprint
from app.modal import db, Transaction, Escrow, Vendor, User, Payout
from app.services.Payaza_service import PayazaServices
from app.routes import unified_data
import uuid_utils as uuid

payaza = Blueprint("payment_out", __name__, "This is for all routes that lead to paying the seller")
pay_Aza = PayazaServices()

@payaza.route('/disburse-funds/<int:escrow_id>', methods=["POST"])
def disburse_funds(escrow_id):
    escrow = Escrow.query.get_or_404(escrow_id)

    # getting the vendors details
    vendor = Vendor.query.filter_by(id=escrow.seller_id)
    # getting user details
    seller = User.query.filter_by(id=vendor.user_id)

    if escrow.status != "READY FOR PAYOUT":
        return jsonify({
            "error": "Escrow conditions not fully net"
        })

    if Payout.query.filter_by(escrow_id=escrow_id, status="SUCCESSFUL").first():
        return jsonify({"error": "Payout already completed for this escrow"}), 400

    # verify bank details. pls confirm well later
    data = {vendor.account_number, vendor.bank_code}
    if not is_verify_seller_bank(data):
        return jsonify({
            "error": "Invalid Account Number",
            "message": "Can not process the payout"
        })

    tx_ref = f"PAY-{escrow_id}-{uuid.uuid7().hex[:6]}"
    payload = {
        "transaction_type": "mobile_money",
            "service_payload": {
                "payout_amount": escrow.amount,
                "transaction_pin": 218056,
                "account_reference": tx_ref,
                "country": "NGA",
                "currency": "MGN",
                "payout_beneficiaries": [
                    {
                        "credit_amount": escrow.amount,
                        "account_name": vendor.account_name,
                        "account_number": vendor.account_number,
                        "account_name": vendor.account_name,
                        "bank_code": vendor.bank_code,
                        "narration": "Tesrest",
                        "transaction_reference": tx_ref,
                        "sender": {
                            "sender_name": seller.name,
                            "sender_id": seller.id,
                            "sender_phone_number": seller.phone_number,
                            "sender_address": vendor.business_phone
                        }
                    }
                ]
            }
        }
    
    # updating payout model
    response = pay_Aza.initiatae_transfer(payload)

    new_payout = Payout(
        escrow_id=escrow.id,
        seller_id=escrow.seller_id,
        amount=escrow.amount,
        currency=escrow.currency,
        status="processing",
        reference=tx_ref
    )
    db.session.add(new_payout)
    db.session.commit()

    return jsonify(response)

def release_escrow(escrow_id):
    escrow = Escrow.query.get_or_404(escrow_id)

    # getting the vendors details
    vendor = Vendor.query.filter_by(id=escrow.seller_id)
    # getting user details
    seller = User.query.filter_by(id=vendor.user_id)

    # to check escrow balance
    balance_info = pay_Aza.get_vault_balance()
    available = balance_info.get('data', {}).get('available_balance', 0)

    # Note this condition is onky true if the somethis is wrong during testing
    if available < escrow.amount:
        return jsonify({
            "error": "Insufficient Fund"
        }), 400
    
    # CHECKING CONDITIONS
    if all(s.is_fulfilled for s in escrow.statements):
        return jsonify({
            "error": "Can not release funds, Some contracts statements are not yet fulfilled"
        }), 400

    payout_ref = f"RELEASE_{escrow_id}"
    payload = {
        "service_payload": {
            "payout_amount": escrow.amount,
            "transaction_pin": 218056,
            "account_reference": payout_ref,
            "country": "NGA",
            "currency": "MGN",
            "payout_beneficiaries": [
                {
                    "credit_amount": escrow.amount,
                    "account_name": vendor.account_name,
                    "account_number": vendor.account_number,
                    "account_name": vendor.account_name,
                    "bank_code": vendor.bank_code,
                    "narration": "Tesrest",
                    "transaction_reference": payout_ref,
                    "sender": {
                        "sender_name": seller.name,
                        "sender_id": seller.id,
                        "sender_phone_number": seller.phone_number,
                        "sender_address": vendor.business_phone
                    }
                }
            ]
        }
    }
    result = pay_Aza.initiatae_transfer(payload)

    if result.get('status') == 'success':
        escrow.status = "COMPLETED"
        db.session.commit()
    
    return jsonify(result)


# @payaza.route('/verify-seller-bank', methods=['POST'])
def is_verify_seller_bank(data):
    response = pay_Aza.account_name_enquiry(
        data['bank_code'], 
        data['account_number']
        )
    if response.get("response_code") == 200 and response.get("response_message") == "Approved or completely successful":
        return True
    return False


