import base64


key = "PZ78-PKTEST-A432B0CF-8669-4307-A52E-D5F9DD13ADA7"
key_byte = key.encode('utf-8')
key_64 = base64.b64encode(key_byte)
print(key_64)