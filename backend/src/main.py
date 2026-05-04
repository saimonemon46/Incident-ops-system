from fastapi import FastAPI
from src.database.core import engine, Base
from src.incidents.controller import router as incident_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Ops Incident Management")

# Include modular routers
app.include_router(incident_router)

@app.get("/")
def health_check():
    return {"status": "online", "system": "AI-Ops Core"}