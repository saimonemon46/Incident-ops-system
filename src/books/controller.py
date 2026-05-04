from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_all():
    return {"message": "Get all items"}
