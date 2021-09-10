from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer,Boolean, ForeignKey

class Tables(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    status = Column(Boolean)
    user_id = Column(Integer, ForeignKey( "user.id", ondelete = 'cascade'), nullable=True)
    user = relationship("User")