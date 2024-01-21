import logging


from fastapi import FastAPI
from mangum import Mangum


from app.models import profile
from app.core.database import engine
from app.routes.profile_route import profile_router
from app.routes.payment_route import payment_router
from app.routes.card_route import card_router
from app.routes.user_route import user_router
from app.routes.payout_route import payout_router


app = FastAPI(
    title="Profile Service",
    description="Thelima profile service",
    version="1.0.0",
)

profile.Base.metadata.create_all(bind=engine)

handler = Mangum(app)


# Index health check
@app.get('/')
def index():
    return {"message": "Profile service"}


app.include_router(profile_router)
app.include_router(payment_router)
app.include_router(card_router)
app.include_router(user_router)
app.include_router(payout_router)


# TODO: To receive Profile creation event from Authentication service