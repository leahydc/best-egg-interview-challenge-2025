from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.package import Package, SortBy, PackageStatus
from app.services.package_service import get_all_packages, get_package_by_tracking_id

# Router class for calls related to /packages
router = APIRouter()

# GET router to get list of all packages from mock API
@router.get("/packages", response_model=List[Package])
def list_packages(
        status: Optional[PackageStatus] = Query(None, description="Filter by package status"),
        sort: Optional[SortBy] = Query(None, pattern="^(eta|last_updated)$", description="Sort by 'eta' or 'last_updated'")
):
    try:
        return get_all_packages(status=status, sort_by=sort)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET router to get list of all packages from mock API
@router.get("/packages/{tracking_id}", response_model=Package)
def get_package(tracking_id: str):
    try:
        package = get_package_by_tracking_id(tracking_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    return package