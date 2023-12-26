from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
class User(BaseModel):
    _id: ObjectId
    username: str
    password: str
    email: str
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    disabled: Optional[bool] = None
    
class UserInDB(User):
    hashed_password: str