import json


from fastapi import HTTPException
from fastapi.responses import JSONResponse
import sqlalchemy
from sqlalchemy.orm import joinedload


from ..models.profile import Profile


class ProfileService:
    def create_profile(profile, db):
        try:
            profile = Profile(
                auth_id=profile.auth_id,
                full_name=profile.full_name,
                email=profile.email,
                phone_number=profile.phone_number,
                email_verified=profile.email_verified,
                role=profile.role
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)

        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Profile already existed"
            )
        else:
            return profile

    def get_profile(auth_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).options(
            joinedload(Profile.places)).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        return profile

    def update_profile(auth_id, profile, db):
        data = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if data is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        for field, value in profile.dict(exclude_unset=True).items():
            setattr(data, field, value)

        db.commit()
        db.refresh(data)

        return {"message": "Profile updated successfully"}
    
    def update_profile_status(auth_id, status, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        profile.status = status.status
        # setattr(profile, 'status', status)
        db.commit()

        return {"message": "Profile status updated successfully"}
