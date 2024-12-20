from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, validator

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values):  # Accept 'values' and 'field' parameters
        if isinstance(v, ObjectId):
            return str(v)  # Convert ObjectId to string directly
        if isinstance(v, str):
            # Ensure the string is a valid ObjectId
            try:
                ObjectId(v)  # Validate that it's a valid ObjectId string
                return v
            except Exception:
                raise ValueError("Invalid ObjectId string")
        raise ValueError("Invalid ObjectId type")
    
class UserBase(BaseModel):
    email: str
    name: str
    user_id:str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class User(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  
    user_id:str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
