from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,ForeignKey,Integer,String

class Supplies(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    modicum = Column(Integer)
    on_hold = Column(Integer)

class SuppliesPlate(Base):
    __tablename__ = 'supplies_plate'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    food_plate_id = Column(Integer, ForeignKey( "food_plate.id", ondelete = 'cascade'))
    supplies_id = Column(Integer, ForeignKey( "supplies.id", ondelete = 'cascade'))
    food_plate = relationship("FoodPlate")
    supplies = relationship("Supplies")
