from typing import Annotated
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session
from app.core.authenticate import get_current_user
from app.payment.utils import PaymentUtil
from app.schemas.payment import PaymentModel
from app.services.card_service import CardDetailService
from .card_route import get_card_details
from ..core.database import get_db
from app.routes.user_route import credit_user_dashboard

from fastapi import HTTPException

payment_router = APIRouter(prefix='/api/v1/payment')

@payment_router.post('/charge', status_code=status.HTTP_201_CREATED, tags=['Payment Charge Card'])
async def charge_user_card(payment_details: dict, db: Session = Depends(get_db)):
    body = {"email": payment_details.get("email")}
    card_details = await get_card_details(body, db)

    if card_details is None:

        raise HTTPException(status_code=404, detail="Kindly provide your card details")

    payment_details.update(card_details)

    return PaymentUtil.make_charge_request(payment_details)



@payment_router.post('/validate', status_code=status.HTTP_201_CREATED, tags=['Payment Validate'])
async def validate_user_payment(validate_data: dict, db: Session = Depends(get_db)):

    response = PaymentUtil.make_validate_request(validate_data)

    if response.status_code in [201, 200]:
            
        data = {
            "email": response.json()["data"]["customer"]["email"],
            "amount": int(response.json()["data"]["amount"])
        }
        is_sucessful = await credit_user_dashboard(data, db)
        print(is_sucessful)
        if is_sucessful:
            logging.info("User is credited!!!")
        else:
            logging.info(f"User {data['email']} is not credited")
    
    return  response.json()