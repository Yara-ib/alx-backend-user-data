#!/usr/bin/env python3
""" Authentication Module """
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Returns a salted hashed password of the added password."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Gets a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initiating instances method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")

        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Check user's credentials."""
        try:
            user = self._db.find_user_by(email=email)
            x = bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)
            return x
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for the user"""
        try:
            session_id = _generate_uuid()
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Get a user from a session_id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id, hashed_password=_hash_password(password)
                )
            self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError
