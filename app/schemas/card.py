from datetime import date
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, Field, EmailStr

class CardDetails(BaseModel):
    card_number: Optional[str] = Field(None, description="User's card number.")
    cvv: Optional[str] = Field(None, description="User's card cvv.")
    expiry_month: Optional[str] = Field(None, description="User's card expiry month")
    expiry_year: Optional[str] = Field(None, description="User's card expiry year")

    class Config:
        # Exclude fields that shouldn't be updated - subject to change
        exclude = {"cvv", "card_number", "expiry_year", "expiry_month"}