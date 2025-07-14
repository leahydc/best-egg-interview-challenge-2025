from fastapi import APIRouter, HTTPException
from typing import List
from app.models.carrier import Carrier
from app.services.carrier_service import get_all_carriers

router = APIRouter(
    prefix="/carriers",
    tags=["Carriers"]
)

@router.get(
    "",
    response_model=List[Carrier],
    summary="List all carriers",
    description="Fetch a list of all available carriers from the mock API."
)
def list_carriers():
    """
    Retrieve all carriers from the mock API.
    Returns a list of `Carrier` objects.
    """
    try:
        return get_all_carriers()
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
