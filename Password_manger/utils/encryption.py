import json
from cryptography.fernet import Fernet

def generate_key():
    """Generate a key for encryption and decryption"""
    key = Fernet.generate_key()

    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the key from the file
    we here have issues with key
    """
    with open("key.key", "rb") as key_file:
        key = key_file.read().decode('utf-8')
    print(type(key))
    if key:  
        return json.loads(key)
    else:
        return None


def encrypt(password, key):
    """Encrypt a password using the provided key"""
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(password.encode())
    return cipher_text

def decrypt(encrypted_password, key):
    """Decrypt an encrypted password using the provided key"""
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(encrypted_password)
    return plain_text.decode()



