import base64


key = "PZ78-PKTEST-A7A58B61-3673-4E8C-8C36-63495CC2F5B7"
key_byte = key.encode('utf-8')
key_64 = base64.b64encode(key_byte)
print(key_64)