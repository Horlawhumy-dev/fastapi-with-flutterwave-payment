

from fastapi import HTTPException


from app.models.profile import Place, Profile


class PlaceService:
    def add_place(auth_id, place, db):
        # query profile data
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        place = Place(name=place.name, address=place.address,
                      profile_id=profile.id)

        db.add(place)
        db.commit()
        db.refresh(place)

        return place

    def remove_place(auth_id, place_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        place = db.query(Place).filter(Place.id == place_id,
                                       Place.profile_id == profile.id).first()

        if place is None:
            raise HTTPException(
                status_code=404, detail="Place not found for the specified profile")

        db.delete(place)
        db.commit()

        return {"message": "Place deleted successfully"}

    def get_my_places(auth_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        places = db.query(Place).filter(Place.profile_id == profile.id).all()

        return places

    def get_place(auth_id, place_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        place = db.query(Place).filter(Place.id == place_id).first()

        if place is None:
            raise HTTPException(
                status_code=404, detail="Place not found for the specified profile")

        return place
