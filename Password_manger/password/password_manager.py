from datetime import datetime
from models import Password as PasswordModel
from .password_generator import generate_password
from .strength_checker import check_password_strength

class PasswordManager:
    def __init__(self, data_store):
        self.data_store = data_store

    def add_password(self, user, service: str, password: str) -> tuple[bool, str]:
        strength = check_password_strength(password)
        if strength < 3:
            return False, "Password is too weak"
        self.data_store.save_password(user,service,password)
        return True, "Password saved successfully"

    def get_password(self, user, service: str) -> str | None:
        decrypted_password = self.data_store.get_password(user, service)
        if decrypted_password:
            return decrypted_password
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