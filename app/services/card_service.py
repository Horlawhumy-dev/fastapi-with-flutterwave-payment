import json
import sqlalchemy

from datetime import datetime
from sqlalchemy.orm import joinedload

from cryptography.fernet import Fernet
from fastapi import HTTPException

from ..models.card import EncryptedCardDetails
from ..models.user import User

from app.core.config import env_vars
# Define your secret key for encryption (keep this secret!)
SECRET_KEY = env_vars.JWT_KEY_ID
cipher_suite = Fernet(SECRET_KEY)


class CardDetailService:
    def store_card_details(card, db):

        email = card.get("email")

        # Check if the user exists
        user_with_card = db.query(User).filter_by(email=email).first()

        if user_with_card:
            try:
                # Encrypt card details
                encrypted_card = EncryptedCardDetails(
                    card_number=cipher_suite.encrypt(card["card_number"].encode()).decode(),
                    cvv=cipher_suite.encrypt(card["cvv"].encode()).decode(),
                    expiry_month=cipher_suite.encrypt(card["expiry_month"].encode()).decode(),
                    expiry_year=cipher_suite.encrypt(card["expiry_year"].encode()).decode(),
                    date_stored=datetime.now(),
                    user_id=user_with_card.id  # Associate with the user
                )

                # Add the encrypted card to the session
                db.add(encrypted_card)

                # Update the user's encrypted_card_details relationship
                user_with_card.encrypted_card_details = encrypted_card

                # Commit the changes
                db.commit()

                # Refresh the user and encrypted_card objects
                db.refresh(user_with_card)
                db.refresh(encrypted_card)

            except sqlalchemy.exc.IntegrityError:
                # Handle integrity errors (e.g., duplicate card)
                db.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Card already exists"
                )
            except Exception as e:
                # Handle other exceptions
                db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail="Internal Server Error"
                )
        else:
            # Handle case when user does not exist
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Return the encrypted card details
        return encrypted_card


    def get_card(user_email, db):
        user_with_card = db.query(User).\
        filter(User.email == user_email).\
        options(joinedload(User.encrypted_card_details)).\
        first()

        # Access the user's card details
        if user_with_card:
            card = user_with_card.encrypted_card_details
            # card = db.query(EncryptedCardDetails).filter(email == EncryptedCardDetails.owner.email).first()

            if card is None:
                raise HTTPException(status_code=404, detail=f"card not found for the user with email={user_email}")

            else:
                return card

        else:
            return None

    
    def decode_card(encrypted_card):
        if encrypted_card:
            return {
                    "card_number": cipher_suite.decrypt(encrypted_card.card_number).decode(),
                    "cvv": cipher_suite.decrypt(encrypted_card.cvv).decode(),
                    "expiry_month": cipher_suite.decrypt(encrypted_card.expiry_month).decode(),
                    "expiry_year": cipher_suite.decrypt(encrypted_card.expiry_year).decode(),
                    "date_stored": encrypted_card.date_stored
            }

        return encrypted_card
