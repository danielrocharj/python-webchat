from sqlalchemy import Boolean, Column, Integer, String

from app.database.core import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    username = Column(String(40), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean(), default=True)
    admin = Column(Boolean(), default=False)
    # created_at = Column(DateTime, nullable=False, default=)
    # update_at = Column(DateTime, nullable=False, default=)
