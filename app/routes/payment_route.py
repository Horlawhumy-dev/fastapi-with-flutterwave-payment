from typing import Annotated
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session
from app.core.authenticate import get_current_user
from app.payment.utils import PaymentUtil
from app.services.card_service import CardDetailService
from .card_route import get_card_details
from ..core.database import get_db
from app.routes.user_route import credit_user_balance
from app.serializer.charge_serializer import charge_card_seriliazer
from app.serializer.validate_serializer import validate_serializer
from app.schemas.payment import PaymentCharge, PaymentValidate

from fastapi import HTTPException

payment_router = APIRouter(prefix='/api/v1/payment')

@payment_router.post('/charge', status_code=status.HTTP_201_CREATED, tags=['Payment charge card with otp sent to email'])
async def charge_user_card(charge_details: PaymentCharge, db: Session = Depends(get_db)):
    json_payment_details = charge_card_seriliazer(charge_details)
    email = json_payment_details.get("email")
    card_details = await get_card_details(email, db)

    if card_details is None:

        raise HTTPException(status_code=404, detail="Kindly provide your card details")

    json_payment_details.update(card_details)
    del json_payment_details["date_stored"] # not required
    return PaymentUtil.make_charge_request(json_payment_details)



@payment_router.post('/validate', status_code=status.HTTP_201_CREATED, tags=['Payment Validate'])
async def validate_user_payment(validate_data: PaymentValidate, db: Session = Depends(get_db)):
    json_validate_data = validate_serializer(validate_data)
    response = PaymentUtil.make_validate_request(json_validate_data)

    if response.status_code in [201, 200]:
            
        data = {
            "email": response.json()["data"]["customer"]["email"],
            "amount": int(response.json()["data"]["amount"])
        }
        is_sucessful = await credit_user_balance(data, db)
        if is_sucessful:
            logging.info("User balance is credited!!!")
        else:
            logging.info(f"User {data['email']} is not credited")
    
    return  response.json()