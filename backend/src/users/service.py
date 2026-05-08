from sqlalchemy.orm import Session

from src.entities.user import User
from src.users.models import UserCreate
from src.auth import hash_password, verify_password
from src.exceptions import EmailAlreadyExists, UsernameAlreadyExists, InvalidCredentials


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def register_user(db: Session, data: UserCreate) -> User:
    if get_user_by_email(db, data.email):
        raise EmailAlreadyExists(data.email)

    if db.query(User).filter(User.username == data.username).first():
        raise UsernameAlreadyExists(data.username)

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentials()

    return user