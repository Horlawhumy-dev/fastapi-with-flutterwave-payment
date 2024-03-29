from typing import Annotated
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from ..core.database import get_db
from app.services.card_service import CardDetailService
from app.schemas.card import CardDetails
from app.schemas.user import UserModel
from app.serializer.card_serializer import card_serializer

card_router = APIRouter(prefix='/api/v1/card')

# FastAPI endpoint to store encrypted card details
@card_router.post('/', status_code=status.HTTP_201_CREATED, tags=['Card Details'])
async def store_card(card_details: CardDetails, db: Session = Depends(get_db)):
    card = card_serializer(card_details)
    return CardDetailService.store_card_details(card, db)


# GET A Profile
@card_router.get('/', status_code=status.HTTP_200_OK, tags=['Card Detail'])
async def get_card_details(user_email: str, db: Session = Depends(get_db)):
    encrypted_card = CardDetailService.get_card(user_email, db)
    return CardDetailService.decode_card(encrypted_card)