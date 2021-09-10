from fastapi import APIRouter
from .gem.user import user
from .gem.rol import rol
from .gem.reservation import reservation
from .gem.tables import tables
from .gem.supplies import supplies
from .gem.orders import orders
from .gem.food_plate import food_plate

router = APIRouter()
router.include_router(user.router)
router.include_router(rol.router,tags=["admin"])
router.include_router(reservation.router)
router.include_router(tables.router)
router.include_router(supplies.router)
router.include_router(orders.router)
router.include_router(food_plate.router)