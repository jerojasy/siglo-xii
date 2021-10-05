from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from utils.logging import logger
import cx_Oracle

from sqlalchemy.exc import SQLAlchemyError

# engine = create_engine(
#     settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True,
#      connect_args={'connect_timeout': 3}
# )

host='34.125.149.182'
port=1521
sid='xe'
user='C##SIGLOXXI'
password='sigloxxi'
sid = cx_Oracle.makedsn(host, port, sid=sid)

cstr = 'oracle://{user}:{password}@{sid}'.format(
    user=user,
    password=password,
    sid=sid
)

engine =  create_engine(
    cstr,
    # convert_unicode=False,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        logger.error(f'error - {e}')
    finally:
        db.close()





