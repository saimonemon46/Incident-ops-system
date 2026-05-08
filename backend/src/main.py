from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router
from src.database.core import engine, Base


# Import SQLAlchemy models so metadata.create_all() sees them
from src.entities.user import User
from src.entities.incident import Incident

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Incident Ops System",
    description="Real-time incident management — Phase 1",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "version": "1.0.0"}