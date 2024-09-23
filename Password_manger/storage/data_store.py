import json
from utils.encryption import encrypt,decrypt,generate_key

class DataStoreError(Exception):
    pass


class InvalidUsernameError(DataStoreError):
    def __init__(self, username):
        self.username = username
        self.message = f"Invalid username: {username}"


class ServiceNotFoundError(DataStoreError):
    def __init__(self, service):
        self.service = service
        self.message = f"Service not found: {service}"


class PasswordNotFoundError(DataStoreError):
    def __init__(self, username, service):
        self.username = username
        self.service = service
        self.message = f"Password not found for {username} and {service}"


class EncryptionError(DataStoreError):
    def __init__(self, message):
        self.message = message


class DecryptionError(DataStoreError):
    def __init__(self, message):
        self.message = message


class DataStore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.password_key=generate_key()

    def save_password(self, user, service, password):
        if not user.username:
            raise InvalidUsernameError(user.username)
        data = self._load_data()
        if user.username not in data:
            data[user.username] = {}
        try:
            encrypted_password = encrypt(password, self.password_key)
            data[user.username][service] = encrypted_password.decode('utf-8')  # Decode the bytes object to a string
        except Exception as e:
            raise EncryptionError(str(e))
        self._save_data(data)

    def get_password(self, user, service):
        if not user.username:
            raise InvalidUsernameError(user.username)
        data = self._load_data()
        if user.username not in data or service not in data[user.username]:
            raise PasswordNotFoundError(user.username, service)
        try:
            decrypted_data=decrypt(data[user.username][service],self.password_key)
            print(decrypted_data)
            return decrypted_data
        except Exception as e:
            raise DecryptionError(str(e))

    def _load_data(self):
        try:
            with open(self.file_path, 'r') as f:
                data = f.read()
                print("###", data)
                if data:  
                    return json.loads(data)
                else:
                    return {}
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            raise DataStoreError(f"Error loading data: {str(e)}")

    def _save_data(self, data):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            raise DataStoreError(f"Error saving data: {str(e)}")