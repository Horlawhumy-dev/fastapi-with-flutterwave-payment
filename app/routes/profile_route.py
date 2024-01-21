from typing import Annotated
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session


from app.services.profile_service import ProfileService
from app.services.place_service import PlaceService
from ..core.database import get_db
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileUpdateStatus
from app.schemas.place import Place, PlaceCreate
from app.core.authenticate import get_current_user


profile_router = APIRouter(prefix='/api/v1/profile')


# CREATE A Profile
# TODO: This is API should not be exposed. It should be automatically triggered after
# a successful user email verification on the Authentication service.
@profile_router.post('/', status_code=status.HTTP_201_CREATED, tags=['Profiles'])
async def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    return ProfileService.create_profile(profile, db)


# UPDATE A Profile
@profile_router.put('/', status_code=status.HTTP_200_OK, tags=['Profiles'])
async def update_profile(profile: ProfileUpdate, auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return ProfileService.update_profile(auth_id, profile, db)


# UPDATE PROFILE STATUS
@profile_router.patch('/status', status_code=status.HTTP_200_OK, tags=['Profiles'])
async def update_profile_status(status:ProfileUpdateStatus, auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return ProfileService.update_profile_status(auth_id, status, db)

# GET A Profile
@profile_router.get('/', status_code=status.HTTP_200_OK, tags=['Profiles'])
async def get_profile(auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return ProfileService.get_profile(auth_id, db)


# >>>>>>>>>>>>>>>>>PLACE ROUTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@profile_router.post('/place', status_code=status.HTTP_201_CREATED, tags=['Places'])
async def add_place(place: PlaceCreate, auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return PlaceService.add_place(auth_id, place, db)


# GET MY PLACES
@profile_router.get('/place', status_code=status.HTTP_200_OK, response_model=list[Place], tags=['Places'])
async def get_my_places(auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return PlaceService.get_my_places(auth_id, db)


# GET A PLACE
@profile_router.get('/place/{place_id}', status_code=status.HTTP_200_OK, response_model=Place, tags=['Places'])
async def get_place(auth_id: Annotated[str, Depends(get_current_user)], place_id: Annotated[str, Path(description="The ID of the place to retrieve")], db: Session = Depends(get_db)):
    return PlaceService.get_place(auth_id, place_id, db)


# REMOVE A PLACE
@profile_router.delete('/place/{place_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Places'])
async def remove_place(auth_id: Annotated[str, Depends(get_current_user)], place_id: Annotated[str, Path(description="The ID of the place to delete")], db: Session = Depends(get_db)):
    return PlaceService.remove_place(auth_id, place_id, db)
