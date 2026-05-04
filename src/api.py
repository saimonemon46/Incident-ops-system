from fastapi import APIRouter
from src.books.controller import router as book_router
from src.users.controller import router as user_router
from src.auth.controller import router as auth_router

api_router = APIRouter()

api_router.include_router(book_router, prefix="/books", tags=["Books"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
