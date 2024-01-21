import json
from datetime import datetime


from fastapi import HTTPException
from fastapi.responses import JSONResponse
import sqlalchemy
from sqlalchemy.orm import joinedload


from ..models.user import User, Dashboard


class UserService:
    def create_user(user, db):
        try:
            user = User(
                email=user.get("email"),
                date_joined=datetime.now()
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

    def get_user(email, db):
        profile = db.query(User).filter(User.email == email).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="User not found")

        return profile


    def get_user_dashboard(user_id, db):
        dashboard = db.query(Dashboard).filter(Dashboard.user_id == user_id).first()

        if dashboard is None:
            raise HTTPException(status_code=404, detail="User dashboard not found")

        return dashboard


    def credit_user(email, amount_paid, db):

        try:
            user = db.query(User).filter(email == email).first()

            user.amount += amount_paid
            user.date_credited = datetime.now()
            
            db.add(user)
            db.commit()
            db.refresh(user)

        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(
                status_code=404,
                detail="user not found"
            )

        return True
