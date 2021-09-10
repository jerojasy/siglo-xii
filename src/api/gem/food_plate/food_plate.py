from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.user import UserCreate
from db.session import get_db
from schemas.food_plate import (
    SuppliesList,
    FoodPlateList,FoodPlateCreate,SuppliesPlateCreate
)
from api.deps import get_admin_user,get_client_chofer_user,get_chef_user
from schemas.response import Response_SM
from .controller import (
    get_all_fp_cn, create_fp_cn,
    delete_fp_cn, get_all_sp_fp_cn,
    delete_sp_fp_cn, create_sp_fp_cn,
    get_stock_cn, get_all_fp_wjwt_cn
)

router = APIRouter()

@router.get('/food_plates/get_all_food_plates/',response_model=FoodPlateList,tags=["admin","cliente","cocina"])
def get_all_food_plates(
    page:int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_chofer_user)
):
    fp = get_all_fp_cn(page,db)
    return fp

@router.get('/food_plates/get_all_food_plates_wjwt/',tags=["admin","cliente","cocina"])
def get_all_food_plates_wjwt(
    db: Session = Depends(get_db)
):
    fp = get_all_fp_wjwt_cn(db)
    return fp

@router.get('/food_plates/get_stock/',tags=["admin","cliente","cocina"])
def get_stock(
    food:int,
    db: Session = Depends(get_db)
):
    fp = get_stock_cn(food,db)
    return fp

@router.post("/food_plates/create_food_plates/", response_model = Response_SM,tags=["admin","cocina"])
def create_food_plates(
    food_plate: FoodPlateCreate, 
    db:Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    response = create_fp_cn(food_plate,db)
    return response

@router.delete('/food_plates/delete_food_plates/',response_model=Response_SM,tags=["admin","cocina"])
def delete_food_plates(
    id:int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    response = delete_fp_cn(id,db)
    return response

@router.get('/supplies_food_plates/get_all_supplies_food_plates/',response_model=List[SuppliesList],tags=["admin","cocina"])
def get_all_supplies_food_plates(
    food_plate_id:int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    fp = get_all_sp_fp_cn(food_plate_id,db)
    return fp

@router.delete('/supplies_food_plates/delete_supplies_food_plates/',response_model=Response_SM,tags=["admin","cocina"])
def delete_supplies_food_plates(
    id:int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    response = delete_sp_fp_cn(id,db)
    return response


@router.put("/food_plates/update_supplies_food_plates/", response_model = Response_SM,tags=["admin","cocina"])
def update_supplies_food_plates(
    supplies_fp:List[SuppliesPlateCreate], 
    db:Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    response = create_sp_fp_cn(supplies_fp,db)
    return response


