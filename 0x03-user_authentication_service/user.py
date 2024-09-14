#!/usr/bin/env python3
""" User Module """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import VARCHAR


Base = declarative_base()


class User(Base):
    """User class"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(250), nullable=True)
    hashed_password = Column(VARCHAR(250), nullable=True)
    session_id = Column(VARCHAR(250))
    reset_token = Column(VARCHAR(250))
