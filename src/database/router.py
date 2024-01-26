
from fastapi import APIRouter

router = APIRouter()

@router.get("/database")
def example():
  return {
    "route": "database"
  }