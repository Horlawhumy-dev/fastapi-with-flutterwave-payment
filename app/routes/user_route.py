from typing import Annotated
import logging
import json
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session
from app.core.authenticate import get_current_user
from app.services.card_service import CardDetailService
from .card_route import get_card_details
from ..core.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserModel
from app.schemas.payment import Credit
from app.serializer.user_serializer import user_serializer

user_router = APIRouter(prefix='/api/v1/user')

@user_router.get('/', status_code=status.HTTP_200_OK, tags=['User Account Fetch'])
async def get_user(email: str, db: Session = Depends(get_db)):
    return UserService.get_user(email, db)


@user_router.post('/credit', status_code=status.HTTP_200_OK, tags=['User Balance Credit'])
async def credit_user_balance(json_data: dict, db: Session = Depends(get_db)):
    return UserService.credit_user(json_data["email"], json_data["amount"], db)

@user_router.post('/', status_code=status.HTTP_201_CREATED, tags=['User Create Account'])
async def create_user(data: UserModel, db: Session = Depends(get_db)):
    json_data = user_serializer(data)
    return UserService.create_user(json_data, db)
