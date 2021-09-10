from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from db.session import get_db
from schemas.response import Response_SM
from schemas.tables import TablesBase, TablesUpdate,ListTables
from schemas.token import TokenUser
from schemas.user import UserCreate
from core.security import create_access_token
from api.deps import get_admin_user, get_client_user
from .controller import (
    get_all_tables, create_tables,
    delete_tables_cn, update_table_cn
)
router = APIRouter()

@router.post("/tables/create_tables/", response_model = Response_SM, tags=["admin"])
def reservation_create(
        tables: TablesBase, 
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_client_user)
    ):
    response = create_tables(tables, db)
    return response

@router.get("/tables/get_all_tables/", response_model = ListTables,tags=["admin"])
def get_all_reservation(
        page: int,
        db: Session = Depends(get_db)
        # current_user: UserCreate = Depends(get_admin_user)
    ):
    reservation = get_all_tables(page, db)
    return reservation

@router.delete("/tables/delete_tables/", response_model = Response_SM, tags=["admin"])
def delete_tables(
        id: int,
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_admin_user)
    ):
    response = delete_tables_cn(id, db)
    return response

@router.put("/tables/update_tables/", response_model = Response_SM,tags=["admin"])
def update_reservation(
        upd_table: TablesUpdate,
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_client_user)
    ):
    response = update_table_cn(upd_table, db)
    return response

