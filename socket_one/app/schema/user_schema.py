from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):
    id: str
    name: str
    email: str
    photo: str | None = None
    created_at: datetime
    updated_at: datetime

class UserBaseSchema(BaseModel):
    name: str
    email: str
    photo: str | None = None
    created_at: datetime = datetime.now()
    updated_at: datetime  = datetime.now()

class CreateUserSchema(UserBaseSchema):
    name: str = Field()
    email: EmailStr = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sayed Abdul Karim",
                "email": "sakarim9124@gmail.com",
                "password": "password",
            }
        }
    }

class UpdateUser(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
