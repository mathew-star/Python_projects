from datetime import datetime
from models import Password as PasswordModel
from .password_generator import generate_password
from .strength_checker import check_password_strength
from utils.encryption import encrypt, decrypt,generate_key

class PasswordManager:
    def __init__(self, data_store):
        self.data_store = data_store
        self.password_key=generate_key()

    def add_password(self, user, service: str, password: str) -> tuple[bool, str]:
        strength = check_password_strength(password)
        if strength < 3:
            return False, "Password is too weak"
        
        encrypted_password = encrypt(password,self.password_key)
        self.data_store.save_password(service, encrypted_password, user.username)
        return True, "Password saved successfully"

    def get_password(self, user, service: str) -> str | None:
        password_model = self.data_store.get_password(user.username, service)
        if password_model:
            return decrypt(password_model.encrypted_password,self.password_key)
        return None

    def generate_password(self, length: int = 12) -> str:
        return generate_password(length)

    def update_password(self, user, service: str, new_password: str) -> tuple[bool, str]:
        strength = check_password_strength(new_password)
        if strength < 3:
            return False, "New password is too weak"
        
        password_model = self.data_store.get_password(user.username, service)
        if not password_model:
            return False, "Password not found"
        
        password_model.encrypted_password = encrypt(new_password,self.password_key)
        password_model.last_updated = datetime.now()
        self.data_store.save_password(password_model)
        return True, "Password updated successfully"