from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from db.session import get_db
from schemas.reservation import (
    ReservationStatus,
    ReservationBase,UpdateReservation, ReservationList
)
from schemas.response import Response_SM
from schemas.user import UserCreate,UserList
from schemas.token import TokenUser
from core.security import create_access_token
from api.deps import get_admin_user, get_client_user
from .controller import (
    create_reservation as create_rsvt,
    get_user_reservation_cn,
    get_all_reservation_cn, get_all_rsvt_status_cn,
    delete_reservation_cn, update_reservation_cn,
    create_reservation_status as create_rsvt_st,
    update_reservation_status_cn as update_rsvt_st_cn,
    delete_reservation_status_cn as delete_rsvt_st_cn
)
router = APIRouter()

@router.get("/reservation/get_all_reservation/", response_model = ReservationList,tags=["admin"])
def get_all_reservation(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    reservation = get_all_reservation_cn(page,db)
    return reservation

@router.get("/reservation/get_reservation_user/", response_model = ReservationList,tags=["cliente"])
def get_user_reservation(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserList = Depends(get_admin_user)
):
    reservation = get_user_reservation_cn(current_user,page,db)
    return reservation

@router.post("/reservation/reservation_create/", response_model = Response_SM,tags=["admin","cliente"])
def reservation_create(
    rsvt: ReservationBase, 
    db:Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    '''La creacion de reserva se permite segun la cantidad de mesas disponibles'''
    response = create_rsvt(rsvt,db)
    return response

@router.delete("/reservation/delete_reservation/", response_model = Response_SM,tags=["admin","cliente"])
def delete_reservation(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    response = delete_reservation_cn(id, db)
    return response

@router.put("/reservation/update_reservation/", response_model = Response_SM,tags=["admin","cliente"])
def update_reservation(
    upd_rsvt: UpdateReservation,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    response = update_reservation_cn(upd_rsvt, db)
    return response

########################
## RESERVATION STATUS ##
########################

@router.get("/reservation/get_all_reservation_status/", response_model = List[ReservationStatus],tags=["admin","cliente"])
def get_all_reservation(
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    status = get_all_rsvt_status_cn(db)
    return status

@router.post("/reservation/reservation_status_create/", response_model = Response_SM, tags = ["admin"])
def reservation_status_create(
        rsvt: ReservationStatus, 
        db:Session = Depends(get_db),
        current_user: UserCreate = Depends(get_admin_user)
    ):
    response = create_rsvt_st(rsvt,db)
    return response

@router.put("/reservation/update_reservation_status/", response_model = Response_SM,tags=["admin"])
def update_reservation(
    upd_status: ReservationStatus,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = update_rsvt_st_cn(upd_status, db)
    return response

@router.delete("/reservation/delete_reservation_status/", response_model = Response_SM, tags=["admin"])
def delete_reservation(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = delete_rsvt_st_cn(id, db)
    return response
