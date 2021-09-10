from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from utils.logging import logger
from utils.pagination import paginate
from schemas.food_plate import FoodPlateCreate,SuppliesPlateCreate
from schemas.response import Response_SM
from models import FoodPlate,SuppliesPlate,Supplies

def get_all_fp_cn(page:int,db:Session):
    fp  = paginate(db.query(FoodPlate),page,100)
    return fp

def get_all_fp_wjwt_cn(db:Session):
    fp = db.query(FoodPlate).all()
    return fp

def get_stock_cn(food:int,db:Session):
    supplies_plate  = db.query(SuppliesPlate).filter(
        SuppliesPlate.food_plate_id == food
    ).all()
    stock = 0
    stock_list = []
    try:
        for sp in supplies_plate:
            quantity_sp = db.query(Supplies.quantity).filter(
                Supplies.id == sp.supplies_id
            ).first()
            logger.info(f'quantity {quantity_sp}')
            logger.info(f'supple {sp}')
            if quantity_sp and isinstance(quantity_sp,tuple):
                stock_dv = int(quantity_sp[0] / sp.quantity)
                stock_list.append(stock_dv)
    except Exception as e:
        logger.info(f'error {e}')
    logger.info(f'supplies {supplies_plate}')
    return {'stock':min(stock_list) if stock_list else 0}
 

def get_all_sp_fp_cn(food_plate_id:int,db:Session):
    sp = db.query(SuppliesPlate).filter(
        SuppliesPlate.food_plate_id == food_plate_id
    ).all()
    return sp

def create_fp_cn(food_plate: FoodPlateCreate, db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        fp_data = FoodPlate(
            name = food_plate.name,
            price = food_plate.price,
            creation = datetime.now()
        )
        db.add(fp_data)
        db.commit()
        db.refresh(fp_data)
        arsene.status = True if fp_data.id else False
        arsene.result = 'success'
        for sp in food_plate.supplies:
            if db.query(Supplies).filter(Supplies.id == sp.id).first():
                sp_date = SuppliesPlate(
                    quantity = sp.quantity,
                    food_plate_id = fp_data.id,
                    supplies_id = sp.id,
                )
                db.add(sp_date)
                db.commit()
                db.refresh(sp_date)
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene  

def create_sp_fp_cn(supplies_fp:List[SuppliesPlateCreate],db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        for sp in supplies_fp:
            if db.query(Supplies).filter(Supplies.id == sp.supplies_id).first():
                sp_date = SuppliesPlate(
                    quantity = sp.quantity,
                    food_plate_id = sp.food_plate_id,
                    supplies_id = sp.supplies_id,
                )
                db.add(sp_date)
                db.commit()
                db.refresh(sp_date)
        arsene.status = True 
        arsene.result = 'success'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene  

def delete_fp_cn(id:int,db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        food_delete = db.query(FoodPlate).filter(FoodPlate.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if food_delete else False
        arsene.result = 'success' if food_delete else 'food plate does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_sp_fp_cn(id:int,db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        food_delete = db.query(SuppliesPlate).filter(SuppliesPlate.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if food_delete else False
        arsene.result = 'success' if food_delete else 'supplies food plate does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene