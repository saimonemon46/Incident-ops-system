from fastapi import FastAPI
from src.api import api_router

app = FastAPI(title="Library API")

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Library API is running"}
