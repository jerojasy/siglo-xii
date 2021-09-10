from sqlalchemy.orm import Session
from utils.logging import logger
from utils.pagination import paginate
from models import User
# from models.rol import Rol
from schemas.user import UserCreate,UserList
from schemas.response import Response_SM
from core.security import verify_password,get_password_hash

def get_by_email(db: Session,email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate(db: Session,email: str, password: str):
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_user(db: Session,obj_in: UserCreate):
    arsene =  Response_SM(status=False,result= '...')
    try:
        db_obj = User(
            email=obj_in.email,name=obj_in.name,
            password=get_password_hash(obj_in.password),
            rol_id=obj_in.rol_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        arsene.status = True if db_obj.id else False
        arsene.result = 'success'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def get_all_user_cn(page,db: Session):
    user  = paginate(db.query(User),page,100)
    return user

def delete_user_cn(id:int,db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        user = db.query(User).filter(User.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if user else False
        arsene.result = 'success' if user else 'user does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_user_cn(upd_user:UserList,db:Session):
    arsene =  Response_SM(status=False,result= '...')
    try:
        user = db.query(User).filter(User.id == upd_user.id).update({
            User.rol_id: upd_user.rol_id,
            User.password: get_password_hash(upd_user.password),
            User.email: upd_user.email
        })
        db.commit()
        db.flush()
        arsene.status = True if user else False
        arsene.result = 'success' if user else 'user does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene