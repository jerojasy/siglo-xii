from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class ReservationStatus(Base):
    __tablename__ = 'reservation_status'
    id = Column(Integer,primary_key = True)
    name = Column(String)
    
class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer,primary_key = True)
    date_applied = Column(DateTime)
    user_id = Column(Integer, ForeignKey( "user.id", ondelete = 'cascade'))
    status_id = Column(Integer, ForeignKey( "reservation_status.id", ondelete = 'cascade'))
    user = relationship("User")
    status = relationship("ReservationStatus")

