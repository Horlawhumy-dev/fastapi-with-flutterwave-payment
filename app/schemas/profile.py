

from datetime import date
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field


# class Profile(BaseModel):
#     id: str
#     auth_id: str
#     full_name: str
#     email: str
#     phone_number: str
#     email_verified: bool 
#     role: str
#     gender: str
#     language: str
#     date_of_birth: str


class ProfileCreate(BaseModel):

    auth_id: str
    full_name: str
    email: EmailStr
    phone_number: str
    email_verified: bool
    role: str


class ProfileStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'
    away = 'away'


class ProfileUpdateStatus(BaseModel):
    status: ProfileStatus


class ProfileUpdate(BaseModel):
    language: Optional[str] = Field(None, description="User's preferred language.")
    gender: Optional[str] = Field(None, description="User's gender.")
    date_of_birth: Optional[date] = Field(None, description="User's date of birth.")
    # >>>>>>>>>>>>>>TODO: Request for the actual status values to use.>>>>>>>>>>>>>>>>>>>>
    status: Optional[ProfileStatus] = Field(None, description="User's status")
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    city: Optional[str] = Field(None, description="Rider's city of operation.")

    class Config:
        # Exclude fields that shouldn't be updated, like auth_id, id, or roles
        exclude = {"auth_id", "id", "role"}