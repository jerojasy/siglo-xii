from models import Base
from sqlalchemy import Column, Integer,String,DateTime

class FoodPlate(Base):
    __tablename__ = 'food_plate'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    creation = Column(DateTime)