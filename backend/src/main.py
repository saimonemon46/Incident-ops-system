from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import api_router
from src.database.core import engine, Base

# Create DB tables (In production, use Alembic migrations instead of this)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Incident Management System API", version="1.0.0")

# Allow your React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "System is running. No panic required."}