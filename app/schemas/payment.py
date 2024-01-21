
from datetime import date
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field

class PaymentCharge(BaseModel):
    email: EmailStr
    amount: int
    card_number: Optional[str] = Field(None, description="User's card number.")
    cvv: Optional[str] = Field(None, description="User's card cvv.")
    expiry_month: Optional[str] = Field(None, description="User's card expiry month")
    expiry_year: Optional[str] = Field(None, description="User's card expiry year")
    pin: int
    fullname: str


    class Config:
        # Exclude fields that shouldn't be updated - subject to change
        exclude = {"cvv", "card_number", "expiry_year", "expiry_month"}


class PaymentValidate(BaseModel):

    flw_ref: Optional[str]=Field(None, description="Flutterwave Transaction Reference From Charge API")
    otp: Optional[int]=Field(None, description="OTP Sent To User Email")


class Credit(BaseModel):
    email: EmailStr
    amount: Optional[int]=Field(None, description="Amount to credit user")