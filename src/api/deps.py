from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,Header
from db.session import get_db
from core.config import settings
from schemas.user import UserCreate
from schemas.token import TokenData
from utils.logging import logger
from .gem.user.controller import get_by_email

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_token_bearer(token: str = Header(...)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError as e:
        logger.error(f'error {e}')
        raise credentials_exception
    return token_data

def get_current_user(
    token_data: str = Depends(get_token_bearer),db: Session = Depends(get_db)
):
    user = get_by_email(db, email=token_data.email)
    if not user:
        raise credentials_exception
    return user

def get_admin_user(
    token_data: str = Depends(get_token_bearer),db: Session = Depends(get_db)
):
    user = get_by_email(db, email=token_data.email) or {}
    if not user:
        raise credentials_exception
    rol = getattr(getattr(user,'rol'),'id',None) 
    if rol is not 1:
        raise credentials_exception
    return user

def get_client_user(
    token_data: str = Depends(get_token_bearer),db: Session = Depends(get_db)
):
    user = get_by_email(db, email=token_data.email) or {}
    if not user:
        raise credentials_exception
    rol = getattr(getattr(user,'rol'),'id',None) 
    if rol not in [1,2]:
        raise credentials_exception
    return user

def get_client_chofer_user(
    token_data: str = Depends(get_token_bearer),db: Session = Depends(get_db)
):
    user = get_by_email(db, email=token_data.email) or {}
    if not user:
        raise credentials_exception
    rol = getattr(getattr(user,'rol'),'id',None) 
    if rol not in [1,2,4]:
        raise credentials_exception
    return user

def get_grocer_user(
    token_data: str = Depends(get_token_bearer),db: Session = Depends(get_db)
):
    user = get_by_email(db, email=token_data.email) or {}
    if not user:
        raise credentials_exception
    rol = getattr(getattr(user,'rol'),'id',None) 
    if rol not in [1,3]:
        raise credentials_exception
    return user

def get_chef_user(
    token_data: str = Depends(get_token_bearer),db: Session = Depends(get_db)
):
    user = get_by_email(db, email=token_data.email) or {}
    if not user:
        raise credentials_exception
    rol = getattr(getattr(user,'rol'),'id',None) 
    if rol not in [1,4]:
        raise credentials_exception
    return user

def get_current_active_user(current_user: UserCreate = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
