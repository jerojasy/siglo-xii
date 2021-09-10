from sqlalchemy.orm import Session
from utils.logging import logger
from utils.pagination import paginate
from schemas.response import Response_SM
from models import Tables
from schemas.tables import TablesBase, TablesUpdate

def count_tables(db:Session):
    count = db.query(Tables).count()
    return count

def get_all_tables(page:int, db: Session):
    tables = paginate(db.query(Tables),page,100)
    return tables

def create_tables(tables: TablesBase, db: Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        table_data = Tables(
            number = tables.number,
            status = tables.status,
            user_id = tables.user_id
        )
        db.add(table_data)
        db.commit()
        db.refresh(table_data)
        arsene.status = True if table_data.id else False
        arsene.result = 'create table successfully' if table_data else 'table cant create'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def delete_tables_cn(id: int, db: Session):
    arsene = Response_SM(status = False, result= '...')
    try:
        table_delete = db.query(Tables).filter(Tables.id == id).delete()
        db.commit()
        db.flush()
        arsene.status = True if table_delete else False
        arsene.result = 'success' if table_delete else 'table does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene

def update_table_cn(table: TablesUpdate, db: Session):
    arsene = Response_SM(status = False, result = '...')
    try:
        tables_data = db.query(Tables).filter(Tables.id == table.id).update({
            Tables.number: table.number,
            Tables.status: table.status,
            Tables.user_id: table.user_id
        })
        db.commit()
        db.flush()
        arsene.status = True if tables_data else False
        arsene.result = 'success' if tables_data else 'table does not exist'
    except Exception as e:
        arsene.result = f'error {e}'
        logger.error(f'error {e}')
    return arsene
