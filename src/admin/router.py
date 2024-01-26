from fastapi import APIRouter

router = APIRouter()

@router.get("/admin")
def getAdmin():
  return {
    "route": "admin"
  } 