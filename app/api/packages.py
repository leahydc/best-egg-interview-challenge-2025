from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.package import Package, SortBy, PackageStatus
from app.services.package_service import get_all_packages, get_package_by_tracking_id

# Router class for calls related to /packages
router = APIRouter()

# GET router to get list of all packages from mock API
@router.get("/packages",
            response_model=List[Package],
            description="Get a list of all packages with optional filtering and sorting.",
            tags=["Packages"])
def list_packages(
        status: Optional[PackageStatus] = Query(
            None,
            description="Filter packages by status",
            example="Delivered"),
        sort: Optional[SortBy] = Query(
            None,
            pattern="^(eta|last_updated)$",
            description="Sort packages by 'eta' (earliest first) or 'last_updated' (latest first)", example="eta")
):
    try:
        return get_all_packages(status=status, sort_by=sort)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET router to get specific package via package ID from mock API
@router.get("/packages/{tracking_id}",
            response_model=Package,
            description="Get a specific package by tracking ID.",
            tags=["Packages"],
            responses={
                404: {"description": "Package not found"},
                200: {
                    "description": "Package found",
                    "content": {
                        "application/json": {
                            "example": {
                                "tracking_id": "PKG123456",
                                "carrier": "UPS",
                                "status": "In Transit",
                                "eta": "2025-06-15T18:00:00Z",
                                "last_updated": "2025-06-12T09:30:00Z",
                                "current_city": "Philadelphia"
                            }
                        }
                    }
                }
            })
def get_package(tracking_id: str):
    try:
        package = get_package_by_tracking_id(tracking_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    return package