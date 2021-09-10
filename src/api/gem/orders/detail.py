from typing import List
from sqlalchemy.orm import Session
from models import FoodPlate,OrdersDetail
from utils.logging import logger
from schemas.orders import OrderDtlOrder

def create_detail_cn(id:int, orders_detail: List[OrderDtlOrder],db:Session):
    logger.info(f'order detail {orders_detail}')
    for od in orders_detail:
        try:
            plate = db.query(FoodPlate).filter(FoodPlate.id == od.food_plate_id).first()
            if plate:
                order_detail_data = OrdersDetail(
                    orders_id = id,
                    food_plate_id = od.food_plate_id,
                    status = 'Creada', quantity = od.quantity
                )
                db.add(order_detail_data)
                db.commit()
                db.refresh(order_detail_data)
        except Exception as e:
            logger.error(f'error {e}')
