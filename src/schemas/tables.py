from typing import Optional, List
from pydantic import BaseModel
from .response import Pagination

class TablesBase(BaseModel):
    number: int 
    status: Optional[bool] = True
    user_id: Optional[int]

class TablesUpdate(TablesBase):
    id: int
    class Config:
        orm_mode = True

class ListTables(Pagination):
    data: List[TablesUpdate]
    class Config:
        orm_mode = True