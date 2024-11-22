from typing import Annotated
from fastapi import Depends, FastAPI, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select
import psycopg2


app = FastAPI()


class UserDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    username: str = Field(index=True)
    email: str
    address: str
    password: str
    account_name: str
    account_number: Annotated[int, Field(ge=10)]
    bank_name: str
    account_type: str
    
#This is not a best practice, please use .evn    
password = "password%4012345" 
POSTGRES_DATABASE_URL = f'postgresql+psycopg2://postgres:{password}@localhost:5432/xpense_db'
 
engine = create_engine(POSTGRES_DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#session = Session(engine)  
  
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    
@app.post("/users/")
def create_user(user: UserDB, session: SessionDep) ->UserDB:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[UserDB]:
    
    statement = select(UserDB).offset(offset).limit(limit)
    
    users = session.exec(statement).all()
    return users