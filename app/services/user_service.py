import json
from datetime import datetime


from fastapi import HTTPException
from fastapi.responses import JSONResponse
import sqlalchemy
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.exc import NoResultFound

from ..models.user import User


class UserService:
    def create_user(data, db: Session):
        try:
            user = User(
                email=data.get("email"),
                role=data.get("role", 1),
                date_joined=datetime.now(),
                date_credited=None
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="user already existed"
            )
        else:
            return user

    def get_user(email, db: Session):
        profile = db.query(User).filter(User.email == email).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="User not found")

        return profile


    def credit_user(email, amount_paid, db: Session):
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.amount += amount_paid
                user.date_credited = datetime.now()

                db.commit()
                db.refresh(user)
                return True

        except NoResultFound:
            db.rollback()
            return False

