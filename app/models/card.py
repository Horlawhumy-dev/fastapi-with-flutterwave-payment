from uuid import uuid4


from sqlalchemy import Boolean, Column, Date, String, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Session


from ..core.database import Base


class EncryptedCardDetails(Base):
    __tablename__ = "encrypted_card_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
            nullable=False, unique=True, index=True)    
    # email = Column(String, nullable=False, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), unique=True, nullable=True)  # Allow for nullable foreign key
    card_number = Column(String, nullable=False)
    cvv = Column(String, nullable=False)
    expiry_month = Column(String, nullable=False)
    expiry_year = Column(String, nullable=False)
    date_stored = Column(Date, nullable=True)

     # Define the back reference to the User model
    user = relationship("User", back_populates="encrypted_card_details")