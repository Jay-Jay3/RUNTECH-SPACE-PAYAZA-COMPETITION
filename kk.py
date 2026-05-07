import base64


key = "PZ78-PKTEST-7A36FB93-83BE-4B95-9846-BB797E391339"
key_byte = key.encode('utf-8')
key_64 = base64.b64encode(key_byte)
print(key_64)


# PZ78-PKTEST-7A36FB93-83BE-4B95-9846-BB797E391339



# The generated account
# {
#     "message": "Virtual Account generated successfully",
#     "data": {
#         "account_name": "Payaza(Test Reserved VA)",
#         "account_number": "3330962332",
#         "account_type": "Static",
#         "bank_name": "GLOBUS BANK",
#         "account_reference": "accRef123",
#         "account_expired": false,
#         "message": "Virtual Account generated successfully"
#     },
#     "success": true
# }