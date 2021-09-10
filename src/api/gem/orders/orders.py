from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from db.session import get_db
from schemas.orders import (
    OrdersBase, OrdersUpdate, OrderCreateOrders, OrdersInfo,
    OrdersDetailBase, OrdersDetailUpdate, OrderDtlOrder,
    OrdersCompletedBase, OrdersCompletedUpdate,OrdersDetailCompletedUpdate,
    OrdersDetailCompletedBase, OrdersDetailCompletedUpdate,
    OrderList,ListOrdersDetail,ListOrdersCompleted,ListOrdersDetailCompleted
)
from schemas.response import Response_SM
from schemas.user import UserCreate,UserList
from schemas.token import TokenUser
from core.security import create_access_token
from api.deps import get_admin_user, get_client_user, get_chef_user
from .detail import create_detail_cn
from .controller import (
    get_all_orders_cn, create_orders, update_orders_cn, delete_orders_cn,
    get_all_orders_detail_cn as get_orders_detail,
    create_orders_detail, update_orders_detail_cn,
    delete_orders_detail_cn, get_orders_detail_fo_cn,
    get_all_orders_completed_cn as get_orders_completed,
    create_orders_completed, update_orders_completed_cn,
    delete_orders_completed_cn, get_order_info_cn,
    update_orders_status, orders_change_status_cn,
    get_all_orders_status_cn, 
    get_all_orders_creadas_cn, get_all_orders_en_preparacion_cn,
    get_all_orders_detail_completed_cn as get_ords_detail_cmp,
    create_orders_detail_completed, create_orders_ocd,
    update_orders_detail_completed_cn as upd_ords_detail_completed,
    delete_orders_detail_completed_cn as dlt_ords_detail_completed
)
router = APIRouter()

@router.get("/orders/get_all_orders/",response_model=OrderList,tags=["admin"])
def get_all_orders(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    orders = get_all_orders_cn(page,db)
    return orders

@router.get("/orders/get_all_orders_status/",tags=["admin"])
def get_all_orders_status(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    orders = get_all_orders_status_cn(page,db)
    return orders

@router.get("/orders/get_all_orders_creadas/",response_model=OrderList,tags=["admin"])
def get_all_orders_creadas(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    orders = get_all_orders_creadas_cn(page,db)
    return orders

@router.get("/orders/get_all_orders_en_preparacion/",response_model=OrderList,tags=["admin"])
def get_all_orders_en_preparacion(
    page: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    orders = get_all_orders_en_preparacion_cn(page,db)
    return orders

@router.get("/orders/get_order_info/",response_model=OrdersInfo, tags=["admin"])
def get_order_info(
    id: int,
    db: Session = Depends(get_db),
    # current_user: UserCreate = Depends(get_admin_user)
):
    orders = get_order_info_cn(id,db)
    return orders

@router.post("/orders/orders_create/", response_model = Response_SM,tags=["admin","cliente"])
def orders_create(
    order: OrdersBase, 
    db:Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    response = create_orders(order, db)
    return response

@router.post("/orders/orders_create_ocd/",tags=["admin","cliente"])
def orders_create_ocd(
    order: OrderCreateOrders, 
    db:Session = Depends(get_db),
): 
    response = create_orders_ocd(order, db)
    if not response.status:
        raise HTTPException(status_code=400, detail=response.result)
    return response

@router.put("/orders/orders_update_ocd/",tags=["admin","cliente"])
def orders_update_ocd(
    order: List[OrderDtlOrder], id:int ,
    db:Session = Depends(get_db)
): 
    update_orders_status(id,1,db)
    response = create_detail_cn(id,order,db)
    return {"status":True}

@router.put("/orders/orders_change_status/",tags=["admin","cliente"])
def orders_change_status(
    id:int ,
    status_id : int,
    current_user: UserCreate = Depends(get_chef_user),
    db:Session = Depends(get_db)
): 
    response = orders_change_status_cn(id,status_id,db)
    return response

@router.delete("/orders/delete_orders/", response_model = Response_SM,tags=["admin","cliente"])
def delete_orders(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_client_user)
):
    response = delete_orders_cn(id, db)
    return response

@router.put("/orders/update_orders/", response_model = Response_SM,tags=["admin","cliente"])
def update_orders(
    order: OrdersUpdate,
    db: Session = Depends(get_db),
    # current_user: UserCreate = Depends(get_client_user)
):
    response = update_orders_cn(order, db)
    return response

###################
## ORDERS DETAIL ##
###################

@router.get("/orders_detail/get_orders_detail_for_order/",tags=["admin","cliente"])
def get_orders_detail_for_order(
        order_id: int,
        db: Session = Depends(get_db)
    ):
    response = get_orders_detail_fo_cn(order_id, db)
    return response

@router.get("/orders_detail/get_all_orders_detail/", response_model = ListOrdersDetail,tags=["admin","cliente"])
def get_all_reservation(
        page: int,
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_client_user)
    ):
    response = get_orders_detail(page, db)
    return response

@router.post("/orders_detail/orders_detail_create/", response_model = Response_SM, tags = ["admin"])
def orders_detail_create(
        order: OrdersDetailBase, 
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_chef_user)
    ):
    response = create_orders_detail(order,db)
    return response

@router.put("/orders_detail/update_orders_detail/", response_model = Response_SM,tags=["admin"])
def update_detail(
    upd_detail: OrdersDetailUpdate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    response = update_orders_detail_cn(upd_detail, db)
    return response

@router.delete("/orders_detail/delete_orders_detail/", response_model = Response_SM, tags=["admin"])
def delete_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_chef_user)
):
    response = delete_orders_detail_cn(id, db)
    return response

######################
## ORDERS COMPLETED ##
######################

@router.get("/orders_completed/get_all_orders_completed/", response_model = ListOrdersCompleted,tags=["admin","cliente"])
def get_all_orders_completed(
        page: int,
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_client_user)
    ):
    response = get_orders_completed(page, db)
    return response

@router.post("/orders_completed/orders_completed_create/", response_model = Response_SM, tags = ["admin"])
def orders_completed_create(
        order: OrdersCompletedBase, 
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_admin_user)
    ):
    response = create_orders_completed(order,db)
    return response

@router.put("/orders_completed/update_orders_completed/", response_model = Response_SM,tags=["admin"])
def update_completed(
    upd_completed: OrdersCompletedUpdate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = update_orders_completed_cn(upd_completed, db)
    return response

@router.delete("/orders_completed/delete_orders_completed/", response_model = Response_SM, tags=["admin"])
def delete_completed(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = delete_orders_completed_cn(id, db)
    return response

#############################
## ORDERS DETAIL COMPLETED ##
#############################

@router.get("/orders_detail_completed/get_all_orders_detail_completed/", response_model = ListOrdersDetailCompleted,tags=["admin","cliente"])
def get_all_orders_detail_completed(
        page: int,
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_client_user)
    ):
    response = get_ords_detail_cmp(page, db)
    return response

@router.post("/orders_detail_completed/orders_detail_completed_create/", response_model = Response_SM, tags = ["admin"])
def deteil_completed_create(
        order: OrdersDetailCompletedBase, 
        db: Session = Depends(get_db),
        current_user: UserCreate = Depends(get_admin_user)
    ):
    response = create_orders_detail_completed(order,db)
    return response

@router.put("/orders_detail_completed/update_orders_detail_completed/", response_model = Response_SM,tags=["admin"])
def update_detail_completed(
    upd_detail_completed: OrdersDetailCompletedUpdate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = upd_ords_detail_completed(upd_detail_completed, db)
    return response

@router.delete("/orders_detail_completed/delete_orders_detail_completed/", response_model = Response_SM, tags=["admin"])
def delete_completed(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    response = dlt_ords_detail_completed(id, db)
    return response
