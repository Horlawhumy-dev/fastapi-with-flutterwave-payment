from uuid import uuid4
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, String, text, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Session
from enum import Enum as PythonEnum, auto


from ..core.database import Base
from sqlalchemy.orm import relationship

class UserRole(PythonEnum):
    SENDER = auto()
    RIDER = auto()
    ADMIN = auto()

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, index=True)
    amount = Column(Integer, default=0)
    date_credited = Column(Date, nullable=True)
    date_joined = Column(Date, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.SENDER)

    # Define one-to-one relationship to EncryptedCardDetails
    encrypted_card_details = relationship("EncryptedCardDetails", uselist=False, back_populates="user")