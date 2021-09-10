from typing import Optional,List
from pydantic import BaseModel,EmailStr
from .response import Pagination
# Shared properties
class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation
class Login(UserBase):
    password: str

class UserCreate(Login):
    name: str
    rol_id: Optional[int]

class UserList(UserCreate):
    id: int
    class Config:
        orm_mode = True

class UserListPag(Pagination):
    data: List[UserList]
    class Config:
        orm_mode = True