from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.package import Package
from app.services.package_service import get_all_packages, get_package_by_tracking_id

# Router class for calls related to /packages
router = APIRouter()

# GET router to get list of all packages from mock API
@router.get("/packages", response_model=List[Package])
def list_packages(
        status: Optional[str] = Query(None, description="Filter by package status"),
        sort: Optional[str] = Query(None, regex="^(eta|last_updated)$", description="Sort by 'eta' or 'last_updated'")
):
    return get_all_packages(status=status, sort_by=sort)

# GET router to get list of all packages from mock API
@router.get("/packages/{tracking_id}", response_model=Package)
def get_package(tracking_id: str):
    package = get_package_by_tracking_id(tracking_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package
