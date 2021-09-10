from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
from datetime import datetime
from utils.logging import logger
from utils.pagination import paginate
from schemas.user import UserList
from schemas.response import Response_SM
from schemas.reservation import ReservationBase, UpdateReservation, ReservationStatus as ResStatus
from models import Reservation, ReservationStatus
from api.gem.tables.controller import count_tables

def get_all_reservation_cn(page:int, db:Session):
    reservation = paginate(db.query(Reservation),page,100)
    return reservation

def get_user_reservation_cn(user:UserList,page:int, db:Session):
    query = db.query(Reservation).filter(
        Reservation.user_id == user.id
    )
    reservation = paginate(query,page,10)
    return reservation

def get_reservation_day(date,db:Session):
    count = 0
    try:
        count = db.query(Reservation).filter(
            extract('day',Reservation.date_applied ) == date.day,
            extract('month',Reservation.date_applied ) == date.month,
            extract('year',Reservation.date_applied ) == date.year
        ).count()
    except Exception as e:
        logger.error(f'{e}')
    return count

def permission_reservation(day,db:Session):
    tables = count_tables(db) 
    res = get_reservation_day(day ,db)
    logger.info(f'tables count {tables} res count {res}')
    return tables - res

def create_reservation(rsvt: ReservationBase, db:Session):
    arsene = Response_SM(status = False, result = '...')
    try:
    
        prms = permission_reservation(rsvt.date_applied,db)
        if prms >= 1:
            reservation_data = Reservation(
                user_id = rsvt.user_id,
                date_applied = rsvt.date_applied,
                status_id = 1
            )
            db.add(reservation_data)
            db.commit()
            db.refresh(reservation_data)
            arsene.status = True if reservation_data.id else False
            arsene.result = 'success' if reservation_data else 'reservation cant create'
        else:
            arsene.result = 'Day without reservations available'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_reservation_cn(reservation: UpdateReservation, db: Session):
    arsene = Response_SM(status=False,result= '...')
    try:
        reservation_data = db.query(Reservation).filter(Reservation.id == reservation.id).update({
            Reservation.status_id: reservation.status_id
        })
        db.commit()
        db.flush()
        arsene.status = True if reservation_data else False
        arsene.result = 'success' if reservation_data else 'reservation does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_reservation_cn(id: int, db: Session):
    arsene = Response_SM(status = False, result= '...')
    try:
        reservation_delete = db.query(Reservation).filter(Reservation.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if reservation_delete else False
        arsene.result = 'success' if reservation_delete else 'reservation does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

########################
## RESERVATION STATUS ##
########################

def get_all_rsvt_status_cn(db:Session):
    return db.query(ReservationStatus).all()

def create_reservation_status(status: ResStatus, db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        status_data = ReservationStatus(
            name = status.name
        )
        db.add(status_data)
        db.commit()
        db.refresh(status_data)
        arsene.status = True if status_data.id else False
        arsene.result = 'success'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_reservation_status_cn(status: ResStatus, db: Session):
    arsene = Response_SM(status=False,result= '...')
    try:
        status_data = db.query(ReservationStatus).filter(ReservationStatus.id == status.id).update({
            ReservationStatus.name: status.name,
        })
        db.commit()
        db.flush()
        arsene.status = True if status_data else False
        arsene.result = 'success' if status_data else 'reservation status does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_reservation_status_cn(id: int, db: Session):
    arsene = Response_SM(status = False, result= '...')
    try:
        status_delete = db.query(ReservationStatus).filter(ReservationStatus.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if status_delete else False
        arsene.result = 'success' if status_delete else 'reservation status does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene
