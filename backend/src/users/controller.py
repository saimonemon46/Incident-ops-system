from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.core import get_db
from src.users.models import UserCreate, UserLogin, UserResponse, TokenResponse
from src.users import service
from src.auth import create_access_token, get_current_user
from src.entities.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """Create a new account. Returns JWT immediately — no separate login needed."""
    user = service.register_user(db, payload)
    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, user=user)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Exchange email + password for a JWT."""
    user = service.authenticate_user(db, payload.email, payload.password)
    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, user=user)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return current_user