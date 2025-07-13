from typing import List, Any
from fastapi import Depends, HTTPException,status
from app.v1.dependencies.auth import get_current_user
from app.v1.model.user_model import User
from app.v1.scripts.errors import InsufficientPermission

class RoleCheck:
    def __init__(self, role:List[str])->None:
        self.roles = role


    def __call__(self, current_user:User=Depends(get_current_user)) -> Any:
         if current_user.role in self.roles:
             return True
         raise InsufficientPermission()