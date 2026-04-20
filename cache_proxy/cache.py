from typing import Dict,Optional
from dataclasses import dataclass


@dataclass
class CacheEntry:
    status_code: int
    headers: Dict[str,str]
    body: bytes



class DictCache:
    
    def __init__(self):
        self.store: Dict[str,CacheEntry]={}


    def get(self,key:str)->Optional[CacheEntry]:
        return self.store.get(key,None)
    
    def set(self,key:str, value:CacheEntry)->None:
        self.store[key]=value

    def clear(self)->None:
        self.store.clear()
        
    def size(self) -> int:
        return len(self.store)


