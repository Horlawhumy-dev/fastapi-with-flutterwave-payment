from datetime import date
from enum import Enum
from typing import Optional, Union
from sqlalchemy import Boolean, Column, Date
from pydantic import BaseModel, Field, EmailStr
from app.models.user import UserRole

class UserModel(BaseModel):
    email: EmailStr
    role: UserRole

    class Config:
        # Exclude fields that shouldn't be updated - subject to change
        exclude = {"email"}