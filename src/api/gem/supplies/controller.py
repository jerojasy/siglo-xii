from sqlalchemy.orm import Session
from utils.logging import logger
from utils.pagination import paginate
from schemas.supplies import SuppliesBase,Supplies
from schemas.response import Response_SM
from models import Supplies

def get_all_supplies_cn(page:int,db:Session):
    sps  = paginate(db.query(Supplies),page,100)
    return sps

def create_sps_cn(sps:SuppliesBase,db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        sps_data = Supplies(
            name=sps.name,
            description = sps.description,
            quantity = sps.quantity,
            modicum = sps.modicum,
            on_hold = sps.on_hold
        )
        db.add(sps_data)
        db.commit()
        db.refresh(sps_data)
        arsene.status = True if sps_data.id else False
        arsene.result = 'success'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene
    
def update_sps_cn(sps:Supplies,db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        sps_data = db.query(Supplies).filter(Supplies.id == sps.id).update({
            Supplies.name: sps.name,
            Supplies.description: sps.description,
            Supplies.quantity: sps.quantity,
            Supplies.modicum: sps.modicum,
            Supplies.on_hold: sps.on_hold
        })
        db.commit()
        db.flush()
        arsene.status = True if sps_data else False
        arsene.result = 'success' if sps_data else 'supplies does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_sps_cn(id:int,db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        supplies_delete = db.query(Supplies).filter(Supplies.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if supplies_delete else False
        arsene.result = 'success' if supplies_delete else 'supplies does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene
