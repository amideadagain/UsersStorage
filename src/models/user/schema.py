from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class UserInput(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserView(UserInput):
    id: int
    register_date: date


class UserPatch(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    register_date: Optional[date]
