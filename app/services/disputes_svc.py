import requests
import os
import base64
from dotenv import load_dotenv
from app import db
from app.modal import Dispute, Escrow, User

load_dotenv()

class UserServices:
    def __init__(self):
        self.table = "users"
    
    def create_dispute(self, details):
        if not Escrow.query.get(details['escrow_id']):
            return {"error": "This message request is invalid and the escrow does not exist"}
        
        dispute = Dispute.query.filter_by(escrow_id=details['escrow_id'])
        if dispute:
            return {"error": "Dispute already exists"}
        
        new_dispute = Dispute(   
                    escrow_id=details['escrow_id'],
                    reason=details['reason']
        )
        db.session.add(new_dispute)
        db.session.commit()
        return new_dispute
    
    
    
    def update_dispute_resolution(self, id, value):
        dispute = Dispute.query.get(id)
        
        dispute.resolution = value    
        db.session.commit()
        return {
            "message": "The dispute resolution has been added succesfully",
            "dispute": dispute
            }
    
    def update_dispute_opened_by(self, id, value):
        user = User.query.filter_by(id=value['open_by'])
        if not user:
            return {'error': "Invalid User"}
        dispute = Dispute.query.get(id)
        if not dispute:
            return {'error': "Invalid Dispute"}
        dispute.opened_by = dispute.opened_by + " , " + value
        db.session.commit()
        return {
            "message": "Successfully"
        }
    

