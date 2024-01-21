from datetime import date
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    email: EmailStr
    date_joined: Optional[date.Date]

    class Config:
        # Exclude fields that shouldn't be updated - subject to change
        exclude = {"email"}



# class UserPaymentModel(BaseModel):
#     date_joined: Optional[date.Date]

#     class Config:
#         # Exclude fields that shouldn't be updated - subject to change
#         exclude = {"email"}