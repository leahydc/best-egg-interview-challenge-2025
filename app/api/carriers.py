from fastapi import APIRouter
from typing import List
from app.models.carrier import Carrier
from app.services.carrier_service import get_all_carriers
from fastapi import HTTPException

# Router class for calls related to /carriers
router = APIRouter()

# GET router to get list of all carriers from mock API
@router.get("/carriers", response_model=List[Carrier])
def list_carriers():
    try:
        return get_all_carriers()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")