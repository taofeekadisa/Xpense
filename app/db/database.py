from typing import Annotated
from fastapi import Depends, FastAPI, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select
import psycopg2
from app.db.models.user import Users

   
    
#This is not a best practice, please use .evn    
password = "password%4012345" 
POSTGRES_DATABASE_URL = f'postgresql+psycopg2://postgres:{password}@localhost:5432/xpense_db'
 
engine = create_engine(POSTGRES_DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

  
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

    
    
