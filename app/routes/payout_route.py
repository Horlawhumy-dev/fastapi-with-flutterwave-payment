from fastapi import HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, Path, status
from pydantic import EmailStr

from datetime import datetime
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.user import User, UserRole

payout_router = APIRouter(prefix='/api/v1/payout')

def find_user(email, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user

@payout_router.post("/", status_code=status.HTTP_201_CREATED, tags=['Payout to Rider'])
def process_payout(
    rider_email: EmailStr,
    sender_email: EmailStr,
    amount: int,
    success: bool,
    db: Session = Depends(get_db)
):
    try:
        sender = find_user(sender_email, db) #this could be gotten from resquest user instead
        rider = find_user(rider_email, db)

        if not sender or not rider:
            raise HTTPException(status_code=404, detail="Sender or rider not found")

        if sender.amount < amount:
            return {"message": f"Sender's balance ({sender.amount}) is less than the requested amount ({amount})."}
            # raise HTTPException(status_code=400, detail="Kindly top up your balance!")

        if rider.role != UserRole.RIDER:
            return {"message": f"Rider with this email {rider.email} has an invalid role."}
        #     raise HTTPException(status_code=400, detail=f"Rider with this email {rider.email} has an invalid role")


        if success:
            sender.amount -= amount
            rider.amount += amount
            rider.date_credited = datetime.now()

            db.commit()
            db.refresh(sender)
            db.refresh(rider)

            return {"success": success, "message": "Rider balance is credited" if success else "Payment failed"}
        else:
            # Rollback if success condition is not met
            db.rollback()
            raise HTTPException(status_code=400, detail="Payment failed due to a non-success condition")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
