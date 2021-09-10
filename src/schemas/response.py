from typing import Optional
from pydantic import BaseModel

class Response_SM(BaseModel):
    status: bool
    result: str

class Response_SM_ID(BaseModel):
    status: bool
    result: str
    id_rs : Optional[int]

class Pagination(BaseModel):
    previous_page:Optional[int]
    next_page: Optional[int]
    total: Optional[int]
    pages: Optional[int]
