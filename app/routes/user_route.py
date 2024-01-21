from typing import Annotated
import logging
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session
from app.core.authenticate import get_current_user
from app.services.card_service import CardDetailService
from .card_route import get_card_details
from ..core.database import get_db
from app.services.user_service import UserService

user_router = APIRouter(prefix='/api/v1/user')

@user_router.get('/', status_code=status.HTTP_200_OK, tags=['User Fetch'])
async def get_user(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    return UserService.get_user(email, db)


@user_router.post('/credit', status_code=status.HTTP_200_OK, tags=['User Dashboard Fetch'])
async def credit_user_dashboard(data: dict, db: Session = Depends(get_db)):
    return UserService.credit_user(data["email"], data["amount"], db)

@user_router.post('/', status_code=status.HTTP_201_CREATED, tags=['User Create'])
async def get_user(user: dict, db: Session = Depends(get_db)):
    return UserService.create_user(user, db)

