from fastapi import HTTPException  # Use FastAPI's HTTPException, not http.client's
from typing import List, Optional
from app.models.package import Package, PackageStatus, SortBy
from app.models.enriched_package import EnrichedPackage, CityMetadata
from app.services.http_client import MockApiClient

client = MockApiClient()


def get_all_packages(
        status: Optional[PackageStatus] = None,
        sort_by: Optional[SortBy] = None
) -> List[Package]:
    """
    Fetch all packages from the mock API,
    optionally filtered by status and sorted by eta or last_updated.
    """
    data = client.get("/tracking")
    packages = [Package(**item) for item in data.get("packages", [])]

    # Filter by status (case-insensitive)
    if status:
        packages = [pkg for pkg in packages if pkg.status.lower() == status.value.lower()]

    # Sort packages
    if sort_by == SortBy.eta:
        packages.sort(key=lambda x: x.eta)  # Earliest ETA first
    elif sort_by == SortBy.last_updated:
        packages.sort(key=lambda x: x.last_updated, reverse=True)  # Most recent first

    return packages


def get_package_by_tracking_id(tracking_id: str) -> Optional[Package]:
    """
    Retrieve a package by tracking ID.
    """
    data = client.get("/tracking")
    for item in data.get("packages", []):
        if item["tracking_id"] == tracking_id:
            return Package(**item)
    return None


def get_enriched_package(tracking_id: str) -> Optional[EnrichedPackage]:
    """
    Retrieve a package by tracking ID and enrich it with city metadata.
    """
    try:
        data = client.get("/tracking")

        package_entry = next((p for p in data.get("packages", []) if p["tracking_id"] == tracking_id), None)
        if not package_entry:
            return None

        package = Package(**package_entry)
        current_city = package.current_city.lower()

        city_data = client.get(f"/locations/{current_city}")
        city_metadata = CityMetadata(**city_data)

        return EnrichedPackage(package=package, city_metadata=city_metadata)

    except Exception as e:
        print(f"ERROR in get_enriched_package: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
