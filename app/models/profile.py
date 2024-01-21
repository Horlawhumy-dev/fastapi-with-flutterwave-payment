from uuid import uuid4


from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Session


from ..core.database import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                nullable=False, unique=True, index=True)
    auth_id = Column(String, nullable=False, index=True, unique=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone_number = Column(String, default=False)
    email_verified = Column(Boolean, default=False)
    role = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    language = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    status = Column(String, nullable=True)
    city = Column(String, nullable=True)

    # Establishing a one-to-many relationship with the Place table
    places = relationship("Place", back_populates='profile')


class Place(Base):
    __tablename__ = 'places'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Foreign key relationship with the Profile table
    profile_id = Column(UUID(as_uuid=True), ForeignKey(
        "profiles.id"), nullable=False)

    # Establishing the relationship from the Place side
    profile = relationship(Profile, back_populates='places')
