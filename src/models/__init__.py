from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from .rol import Rol
from .user import User
from .tables import Tables
from .food_plate import FoodPlate
from .supplies import Supplies, SuppliesPlate
from .reservation import Reservation, ReservationStatus
from .orders import OrderStatus,Orders, OrdersDetail, OrdersCompleted, OrdersDetailCompleted
