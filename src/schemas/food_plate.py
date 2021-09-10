from typing import Optional, List
from pydantic import BaseModel,validator
from .response import Pagination
from datetime import datetime

class FoodPlateBase(BaseModel):
    name: str
    price: int
    

class SuppliesPlateBase(BaseModel):
    quantity:int

class SuppliesPlateCreate(BaseModel):
    quantity:int
    food_plate_id:int
    supplies_id:int

class SuppliesPlate(SuppliesPlateBase):
    id: int

class SuppliesList(SuppliesPlateCreate):
    id: int
    class Config:
        orm_mode = True

class FoodPlateCreate(FoodPlateBase):
    supplies: List[SuppliesPlate]
    @validator('supplies')
    def supplies_null(cls, v):
        assert len(v) >= 1 ,'must contain 1 supplies' 
        return v

class FoodPlate(FoodPlateBase):
    id: int
    creation: datetime
    class Config:
        orm_mode = True

class FoodPlateList(Pagination):
    data: List[FoodPlate]
    class Config:
        orm_mode = True