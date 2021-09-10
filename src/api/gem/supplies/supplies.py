from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from db.session import get_db
from api.deps import get_grocer_user
from schemas.response import Response_SM
from schemas.supplies import ListSupplies,SuppliesBase,Supplies
from .controller import (
    create_sps_cn,get_all_supplies_cn,
    update_sps_cn,delete_sps_cn
)

router = APIRouter()

@router.get('/get_all_supplies/',response_model=ListSupplies,tags=["admin","bodega"])
def get_all_supplies(
    page:int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_grocer_user)
):
    sps = get_all_supplies_cn(page,db)
    return sps

@router.post('/create_supplies/',response_model=Response_SM,tags=["admin","bodega"])
def create_supplies(
    sps: SuppliesBase,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_grocer_user)
):
    response = create_sps_cn(sps,db)
    return response

@router.put('/update_supplies/',response_model=Response_SM,tags=["admin","bodega"])
def update_supplies(
    sps: Supplies,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_grocer_user)
):
    response = update_sps_cn(sps,db)
    return response

@router.delete('/delete_supplies/',response_model=Response_SM,tags=["admin","bodega"])
def delete_supplies(
    id:int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_grocer_user)
):
    response = delete_sps_cn(id,db)
    return response