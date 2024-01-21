from datetime import date
from enum import Enum
from typing import Optional
from sqlalchemy import Boolean, Column, Date
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserModel(BaseModel):
    email: EmailStr
    role: Optional[UserRole]

    class Config:
        # Exclude fields that shouldn't be updated - subject to change
        exclude = {"email"}
