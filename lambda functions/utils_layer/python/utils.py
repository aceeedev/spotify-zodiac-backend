from Crypto.Cipher import AES

# constants:
redirect_uri: str = 'https://v519b0wsek.execute-api.us-west-1.amazonaws.com/beta/callback'

# helper functions:
def encrypt_text(text: str, key: bytes):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    ciphertext, tag = cipher.encrypt_and_digest(text.encode("utf8"))
    
    return (ciphertext, nonce)

def decrypt_text(encrypted_text: str, key: bytes, nonce: bytes):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(encrypted_text)
    
    return plaintext
