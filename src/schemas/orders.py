from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .response import Pagination

class OrderDtlOrder(BaseModel):
    food_plate_id: int
    quantity: int
    status: str = 'Creada'

class OrdersBase(BaseModel):
    table_id: int
    status_id: int
    creation: datetime

class OrdersInfo(BaseModel):
    table_id: int
    id: int
    status: str
    creation: datetime
    class Config:
        orm_mode = True

class OrderCreateOrders(OrdersBase):
    creation: datetime = datetime.now()
    status_id: int = 1
    orders_detail : List[OrderDtlOrder]

class OrdersUpdate(OrdersBase):
    id: int
    class Config:
        orm_mode = True

class OrdersDetailBase(BaseModel):
    orders_id: int
    food_plate_id: int
    status: str
    quantity: int
    served: datetime

class OrdersDetailUpdate(OrdersDetailBase):
    id: int
    class Config:
        orm_mode = True

class OrdersCompletedBase(BaseModel):
    status: str
    creation: datetime

class OrdersCompletedUpdate(OrdersCompletedBase):
    id: int
    class Config:
        orm_mode = True

class OrdersDetailCompletedBase(BaseModel):
    orders_id: int
    food_plate_id: int
    quantity: int
    served: datetime

class OrdersDetailCompletedUpdate(OrdersDetailCompletedBase):
    id: int
    class Config:
        orm_mode = True




class OrderList(Pagination):
    data: List[OrdersUpdate]
    class Config:
        orm_mode = True

class ListOrdersDetail(Pagination):
    data: List[OrdersDetailUpdate]
    class Config:
        orm_mode = True

class ListOrdersCompleted(Pagination):
    data: List[OrdersCompletedUpdate]
    class Config:
        orm_mode = True

class ListOrdersDetailCompleted(Pagination):
    data: List[OrdersDetailCompletedUpdate]
    class Config:
        orm_mode = True
