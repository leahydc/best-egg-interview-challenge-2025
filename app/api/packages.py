from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.package import Package, SortBy, PackageStatus
from app.models.enriched_package import EnrichedPackage
from app.services.package_service import (
    get_all_packages,
    get_package_by_tracking_id,
    get_enriched_package
)

router = APIRouter(
    prefix="/packages",
    tags=["Packages"]
)

@router.get(
    "",
    response_model=List[Package],
    summary="List packages",
    description="Retrieve a list of all packages with optional filtering by status and sorting by ETA or last updated time."
)
def list_packages(
        status: Optional[PackageStatus] = Query(
            None,
            description="Filter packages by status.",
            example="Delivered"
        ),
        sort: Optional[SortBy] = Query(
            None,
            description="Sort by 'eta' (ascending) or 'last_updated' (descending).",
            example="eta"
        )
):
    """
    Returns a list of packages optionally filtered by status and sorted by ETA or last updated timestamp.
    """
    try:
        return get_all_packages(status=status, sort_by=sort)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/{tracking_id}",
    response_model=Package,
    summary="Get package by ID",
    description="Retrieve a package by its tracking ID.",
    responses={
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
        },
        404: {"description": "Package not found"}
    }
)
def get_package(tracking_id: str):
    """
    Returns a package by tracking ID, or 404 if not found.
    """
    try:
        package = get_package_by_tracking_id(tracking_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    return package


@router.get(
    "/{tracking_id}/enriched",
    response_model=EnrichedPackage,
    summary="Get enriched package",
    description="Retrieve a package along with additional location metadata.",
    responses={
        200: {"description": "Package with location metadata"},
        404: {"description": "Package not found"}
    }
)
def get_enriched_package_by_id(tracking_id: str):
    """
    Returns an enriched package with location metadata, or 404 if not found.
    """
    try:
        enriched = get_enriched_package(tracking_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if not enriched:
        raise HTTPException(status_code=404, detail="Package not found")

    return enriched
