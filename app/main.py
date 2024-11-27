from fastapi import  FastAPI
from app.api.routes.users import user_router
from app.api.routes.expenses import expense_router
from app.db.database import *


app = FastAPI()

app.include_router(user_router, tags=["Users"], prefix="/v1")
app.include_router(expense_router, tags=["Expenses"], prefix="/v1")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()




























































# class HeaderParams(BaseModel):
#     user_agent:Annotated[str,Field()] = None
#     user_ip:Annotated[str,Field()] = None


# class BioDocs(BaseModel):
#     Id_card:bytes
#     passport_page:bytes


# #Example on Response Model No part of our Expense Application API
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: str | None = None


# def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password

# def save_to_db(user:UserIn):
#     hashed_password = fake_password_hasher(user.password)
#     user_to_db = UserInDB(**user.model_dump(), hashed_password = hashed_password)
#     user_to_db = UserInDB(username=user.username, hashed_password = hashed_password, email=user.email, full_name=user.full_name)
#     return user_to_db


# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = save_to_db(user_in)
#     return user_saved

   

# @app.post("/files/")
# async def create_file(docs: Annotated[list[bytes], File()]):
#     for doc in docs:

#         return {"message": "Upload Succesful",
#                 "data":{"doc_size": f"{len(doc)/1000} KB"
#                         }
#                 }
    
    
# @app.post("/uploadfile/")
# async def create_profile(*, first_name:Annotated[str, Form()],
#                          last_name:Annotated[str, Form()], 
#                          Id_card: UploadFile | None = None, passport_page:UploadFile):
#     if not Id_card and  passport_page:
#         return {"message":"Upload Successful",
#             "data":[
#                     {"passport_page":{"filename": passport_page.filename,
#                     "size":f"{passport_page.size/1000} KB",
#                     "type":passport_page.content_type}}]
#             }
#     elif Id_card and passport_page:   
#         return {"message":"Upload Successful",
#                 "data":[{"Id_card":{"filename": Id_card.filename,
#                         "size":f"{Id_card.size/1000} KB",
#                         "type":Id_card.content_type}},
                        
#                         {"passport_page":{"filename": passport_page.filename,
#                         "size":f"{passport_page.size/1000} KB",
#                         "type":passport_page.content_type}}]
#                 }      
        
# class UploadFiles(BaseModel):
#     Id_card:Annotated[UploadFile, File()]
#     passport:Annotated[UploadFile, File()]
#     cert:Annotated[UploadFile, File()]
#     trans:Annotated[UploadFile, File()]
    
       
# @app.post("/uploadfiles/")
# async def create_profile(docs:Annotated[UploadFiles, File()]):
#     return "Upload Successful"



