from fastapi import APIRouter
from src.incidents.controller import router as incidents_router

api_router = APIRouter()
api_router.include_router(incidents_router)