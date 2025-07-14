from typing import List, Optional
from app.models.package import Package, PackageStatus, SortBy
from app.services.http_client import MockApiClient

client = MockApiClient()

# Function to provide a list of all packages from the mock API && filter/sort them based on query params
def get_all_packages(status: Optional[PackageStatus] = None, sort_by: Optional[SortBy] = None) -> List[Package]:
    data = client.get("/tracking")
    packages = [Package(**item) for item in data.get("packages", [])]

    # Filter by status if status query parameter is provided
    if status:
        packages = [pkg for pkg in packages if pkg.status.lower() == status.lower()]

    # Sort by 'eta' or 'last_updated' if sort query parameter is provided
    if sort_by == "eta":
        packages.sort(key=lambda x: x.eta)  # Earliest ETA first
    elif sort_by == "last_updated":
        packages.sort(key=lambda x: x.last_updated, reverse=True)  # Most recent update first

    return packages

# Function to provide a specific package based on tracking ID value from the mock API
def get_package_by_tracking_id(tracking_id: str) -> Optional[Package]:
    data = client.get("/tracking")
    for item in data.get("packages", []):
        if item["tracking_id"] == tracking_id:
            return Package(**item)
    return None