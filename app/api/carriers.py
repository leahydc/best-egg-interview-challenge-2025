from fastapi import APIRouter
from typing import List
from app.models.carrier import Carrier
from app.services.carrier_service import get_all_carriers

# Router class for calls related to /carriers
router = APIRouter()

# GET router to get list of all carriers from mock API
@router.get("/carriers", response_model=List[Carrier])
def list_carriers():
    return get_all_carriers()