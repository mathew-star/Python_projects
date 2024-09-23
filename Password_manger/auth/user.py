import os
import hashlib
from datetime import datetime , timedelta
from models import User as user_model,Session as SessionModel


class User:
    def __init__(self,username:str,password:str):
        self.model=user_model(username=username,password= self.hash_password(password))
        
    def hash_password(self,password:str)->bytes:
        salt=os.urandom(32)
        key= hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt+key
    
    def create_session(self, duration: timedelta = timedelta(hours=1)) -> SessionModel:
        return SessionModel(
            user_name=self.model.username,
            expires_at=datetime.now() + duration
        )
        
    def login(self) -> None:
        self.model.last_login = datetime.now()
        
        
    @property
    def username(self) -> str:
        return self.model.username