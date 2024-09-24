import json
from cryptography.fernet import Fernet

class LoadKeyError(Exception):
    pass

class LoadingKeyException(LoadKeyError):
    def __init__(self,message):
        self.message= message

def generate_key():
    """Generate a key for encryption and decryption"""
    generated_key = Fernet.generate_key()
    try:
        loaded_key=load_key()
        if loaded_key:
            return loaded_key
        else:
            with open("key.key", "wb") as key_file:
                key_file.write(generated_key)
            return generated_key
    except Exception as e:
        raise LoadingKeyException(str(e))
        
    

def load_key():

    """Load the key from the file
    we here have issues with key
    """
    try:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
            if key:
                return key.decode('utf-8')
            else:return None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
            raise DataStoreError(f"Error loading data: {str(e)}")
        
        


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



