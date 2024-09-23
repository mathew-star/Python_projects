from dataclasses import dataclass,field
from datetime import datetime,timedelta
from typing import Optional

@dataclass
class User:
    username:str
    password:bytes
    created_at: datetime=field(default_factory=datetime.now)
    
@dataclass 
class Password:
    service:str
    encrypted_password:bytes
    user_name:str
    created_at:datetime= field(default_factory=datetime.now)
    last_updated: Optional[datetime]=None
    
    
@dataclass
class Session:
    username: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime= field(default_factory=datetime.now)
    is_active: bool = True