from Crypto.Cipher import AES

# constants:
redirect_uri: str = 'https://astrolify.netlify.app'

# helper functions:
def encrypt_text(text: str, key: str):
    cipher = AES.new(key.encode('utf8'), AES.MODE_EAX)
    nonce = cipher.nonce

    ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf8'))
    
    return (ciphertext, nonce)

def decrypt_text(encrypted_text: str, key: str, nonce: str):
    cipher = AES.new(key.encode('utf8'), AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(encrypted_text).decode()
    
    return plaintext
