from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .response import Pagination

class UpdateReservation(BaseModel):
    id: int
    status_id: int

class ReservationBase(BaseModel):
    date_applied: datetime
    user_id: int
    
class Reservation(ReservationBase):
    id: int
    status_id: int
    class Config:
        orm_mode = True

class ReservationList(Pagination):
    data: List[Reservation]
    class Config:
        orm_mode = True

class ReservationStatus(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

