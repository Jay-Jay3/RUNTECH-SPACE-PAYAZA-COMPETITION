from flask import request, jsonify
from flask_smorest import Blueprint
from app.modal import db, Transaction, Escrow, ContractStatement,Vendor, User, Payout
from app.services.Payaza_service import PayazaServices
from app.routes import unified_data
import uuid_utils as uuid
from datetime import datetime

payaza = Blueprint("escrow", __name__, "This is for all routes that lead to creating the escrow and contract")
pay_Aza = PayazaServices()

@payaza.route('/create-escrow', methods=["POST"])
@unified_data
def create_escrow(data):
    escrow_id = data.get('escrow_id')
    
    # creating a new escrow
    new_escrow = Escrow(
        buyer_id=data['buyer_id'],
        seller_id=data['seller_id'],
        amount=data['amount'],
        currency=data['currency'], 
        status="DRAFT"
    )

    db.session.add(new_escrow)
    db.session.flush()

    statement_list = data.get('statements', [])
    for text in statement_list:
        statement = ContractStatement(
            escrow_id=new_escrow.id,
            statement_text=text
        )
        db.session.add(statement)
    
    db.session.commit()
    
    return jsonify({
        "message": "Escrow created successfully",
        "escrow_id": new_escrow.id,
        "statement_count": len(statement_list)
    })


@payaza.route('/fulfill-statement/<statement_id>', methods=["POST"])
def fulfill_statement(statement_id):
    statement = ContractStatement.query.get_or_404(statement_id)

    statement.is_fulfilled = True
    statement.fulfilled_at = datetime.now()

    # to check if, the lst statement, 
    parent_escrow = statement.escrow
    all_done = all(s.is_fulfilled for s in parent_escrow.statements)

    if all_done:
        parent_escrow.status = "READY_FOR_PAYOUT"
        # REMEMBER TO TRIGGER A NOTIFICATION TO SELLER, BUYER AND ADMIN THAT ORDER IS 
        # READY FOR COMPLETION AND PAYMENT IS DUE
    
    db.session.commit()
    return jsonify({
        "status": "Statement Fulfilled",
        "all_fulfilled": all_done
    })


