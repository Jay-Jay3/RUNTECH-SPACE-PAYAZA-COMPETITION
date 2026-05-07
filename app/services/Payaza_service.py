import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

class PayazaServices:
    def __init__(self):
        self.base_url = os.getenv("PAYAZA_BASE_URL")
        self.headers = {
            "Authorization": f"Payaza {os.getenv("PAYAZA_PUBLIC_KEY")}",
            "X-TenantID": os.getenv("PAYAZA_TENANT_ID"),
            "X-ProductID": os.getenv("PAYAZA_PRODUCT_ID"),
            "Content-type": "application/json"
        }

    # Card Charge (POST)
    def card_charge(self, payload):
        url = f"{self.base_url}card/card_charge/"
        response = requests.post(
            url, 
            json={
                "service_payload" : payload,
            },
            headers=self.headers
            )
        return response.json()
    
    # Check card transaction (POST)
    def check_card_status(self, transaction_ref):
        url = f"{self.base_url}card/card_charge/transaction_status"
        payload = {
            "service_payload": {
                "transaction_reference": transaction_ref
                }
            }
        response = requests.post(
            url,
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    # MOMO process 
    # Momo transaction
    def momo_collection(self, payload):
        url = f"{self.base_url}subsidiary/collections/v1/process-collection"
        response = requests.post(
            url,
            json = payload,
            headers=self.headers
        )
        return response.json()
    
    # Test Account Funding 
    def fund_account_by_momo(self, transaction_ref, country_code):
        url = f"{self.base_url}subsidiary/funding/v1/process-collection"
        payload = {
                "transaction_reference": transaction_ref,
                "country_code": country_code
            }
        response = requests.post(
            url,
            json=payload,
            headers=self.headers
        )
        return response.json

    # MOMO transaction status
    def check_momo_transaction_status(self, transaction_ref, country_code):
        url = f"{self.base_url}subsidiary/collections/v1/check-status"
        params = {
            "transaction_reference": transaction_ref,
            "country_code": country_code
        }
        response = requests.get(
            url,
            params=params,
            headers=self.headers
        )
        return response.json()
    
    # Transfers
    # initiate a transfer
    def initiatae_transfer(self, payload):
        url = f"{self.base_url}payout-receptor/payout"
        response = requests.post(
            url, 
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    # to get the account to pay to 
    def get_merchant_details(self):
        url = f"{self.base_url}payaza-account/api/v1/mainaccounts/merchant/enquiry/main"
        response = requests.get(
            url, 
            headers=self.headers
        )
        return response.json()
    
    # To get the status of the transfer
    def get_transfer_status(self, transfer_ref):
        url = f"{self.base_url}payaza-account/api/v1/mainaccounts/merchant/transaction/{transfer_ref}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    # To get the account name
    def account_name_enquiry(self, bank_code, account_number):
        url = f"{self.base_url}payaza-account/api/v1/mainaccounts/merchant/provider/enquiry"
        payload = {
            "service_payload" : {
                "currency": "NGN",
                "bank_code": bank_code,
                "account_number": account_number
            }
        }
        resposne = requests.post(
            url, 
            json=payload,
            headers=self.headers
        )
        return resposne.json()
    
    # VIRTUAL ACCOUNT
    # to create a virtual account
    def create_virtual_account(self, payload, is_statis=False):
        url = f"{self.base}merchant-collection/merchant/virtual_account/generate_virtual_account/"
        response = requests.post(
            url,
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    # to get virtual account status
    def get_virtual_account_status(self, account_number):
        url = f"{self.base_url}merchant-collection/merchant/virtual_account/detail/virtual_account/{account_number}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    # to get the transaction on the virtual account status
    def query_virtual_account_transaction_status(self, transaction_ref):
        url = f"{self.base_url}merchant-collection/transfer_notification_controller/transaction-query"
        params = {"transaction_reference": transaction_ref}
        response = requests.get(
            url,
            params=params,
            headers=self.headers
        )
        return response.json()
    
    # OUR DEFAULT PAYAZA MERCHANT WALLER
    # TO CHECK BALANCE in the local vault
    def get_vault_balance(self):
        url = f"{self.base_url}payaza-account/api/v1/mainaccounts/merchant/enquiry/main"
        response = requests.get(url, headers=self.headers)
        return response.json()

    


















