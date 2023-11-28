from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime

class ContactModel(BaseModel):
    first_name : str = Field(min_length=3)
    last_name : str = Field(min_length=3)
    email : EmailStr
    phone : str = Field(min_length=10, max_length=20)
    #email: str = Field(default = "example@com.ua", regex ="")
    birthday : date
    
class ContactResponse(BaseModel):
    id: int = 1
    first_name : str
    last_name : str
    email: EmailStr
    phone : str
    birthday : date
    create_at: datetime
    update_at: datetime
    user_id : int 
    class ConfigDict:
        from_attributes = True

 
#NEW
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class ConfigDict:
        from_attributes = True



class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


