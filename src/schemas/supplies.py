from .response import Pagination
from typing import List
from pydantic import BaseModel

class SuppliesBase(BaseModel):
    name: str
    description:str
    quantity:int
    modicum:int
    on_hold:int

class Supplies(SuppliesBase):
    id: int
    class Config:
        orm_mode = True

class ListSupplies(Pagination):
    data: List[Supplies]
    class Config:
        orm_mode = True

