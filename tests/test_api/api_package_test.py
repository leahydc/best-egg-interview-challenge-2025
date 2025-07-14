from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

# Test cases for the carriers router


# Test case: list all carriers successfully
@patch("app.api.carriers.get_all_carriers")
def test_list_carriers_success(mock_get_all_carriers):
    mock_get_all_carriers.return_value = [
        {"id": "UPS", "name": "United Parcel Service"},
        {"id": "FEDEX", "name": "FedEx"},
    ]
    response = client.get("/carriers")
    assert response.status_code == 200
    assert response.json() == mock_get_all_carriers.return_value


# Test case: list carriers when no carriers are available
# Would this empty response be considered a valid use case? -- I think yes, it is valid to return an empty list when no carriers are available
@patch("app.api.carriers.get_all_carriers")
def test_list_carriers_empty(mock_get_all_carriers):
    mock_get_all_carriers.return_value = []
    response = client.get("/carriers")
    assert response.status_code == 200
    assert response.json() == []


# Test case: list carriers with 500 service exception
@patch("app.api.carriers.get_all_carriers")
def test_list_carriers_failure(mock_get_all_carriers):
    mock_get_all_carriers.side_effect = Exception("Mock failure")
    response = client.get("/carriers")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}


# Mock data for packages
mock_packages = [
    {
        "tracking_id": "PKG123",
        "carrier": "UPS",
        "status": "In Transit",
        "eta": "2025-07-15T12:00:00Z",
        "last_updated": "2025-07-14T09:00:00Z",
        "current_city": "Philadelphia"
    },
    {
        "tracking_id": "PKG456",
        "carrier": "FedEx",
        "status": "Delivered",
        "eta": "2025-07-12T10:00:00Z",
        "last_updated": "2025-07-13T08:00:00Z",
        "current_city": "New York"
    }
]


# Test cases for the packages router


# Test case: list all packages successfully
def test_list_packages_success():
    with patch("app.api.packages.get_all_packages", return_value=mock_packages) as mock_get:
        response = client.get("/packages")
        assert response.status_code == 200
        assert response.json() == mock_packages
        mock_get.assert_called_once_with(status=None, sort_by=None)


# Test case: list packages successfully with filters
def test_list_packages_with_filters():
    with patch("app.api.packages.get_all_packages", return_value=mock_packages) as mock_get:
        response = client.get("/packages?status=In Transit&sort=eta")
        assert response.status_code == 200
        assert response.json() == mock_packages
        mock_get.assert_called_once_with(status="In Transit", sort_by="eta")


# Test case: list packages with 500 service exception
def test_list_packages_service_exception():
    with patch("app.api.packages.get_all_packages", side_effect=Exception("Mock failure")):
        response = client.get("/packages")
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"


# Test case: get a specific package successfully by tracking ID
def test_get_package_success():
    package = mock_packages[0]
    with patch("app.api.packages.get_package_by_tracking_id", return_value=package) as mock_get:
        response = client.get(f"/packages/{package['tracking_id']}")
        assert response.status_code == 200
        assert response.json() == package
        mock_get.assert_called_once_with(package["tracking_id"])


# Test case: 404 response when package not found
def test_get_package_not_found():
    with patch("app.api.packages.get_package_by_tracking_id", return_value=None):
        response = client.get("/packages/UNKNOWN123")
        assert response.status_code == 404
        assert response.json()["detail"] == "Package not found"


# Test case: package by package_id with 500 service exception
def test_get_package_service_exception():
    with patch("app.api.packages.get_package_by_tracking_id", side_effect=Exception("Mock failure")):
        response = client.get("/packages/PKG123")
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"