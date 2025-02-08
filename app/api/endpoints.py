from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Radiology AI Backend is Running!"}
