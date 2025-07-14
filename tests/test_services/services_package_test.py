import pytest
from unittest.mock import patch, MagicMock
from app.services.package_service import get_all_packages, get_package_by_tracking_id
from app.models.package import Package
from app.services.carrier_service import get_all_carriers
from app.models.carrier import Carrier
from app.services.http_client import MockApiClient
import requests


# Test case: get all carriers successfully
def test_get_all_carriers_success():
    mock_response = {
        "carriers": [
            {"id": "UPS", "name": "United Parcel Service"},
            {"id": "FEDEX", "name": "FedEx"},
        ]
    }

    with patch("app.services.carrier_service.client") as mock_client:
        mock_client.get.return_value = mock_response

        carriers = get_all_carriers()

        assert len(carriers) == 2
        assert all(isinstance(c, Carrier) for c in carriers)
        assert carriers[0].id == "UPS"
        assert carriers[0].name == "United Parcel Service"
        assert carriers[1].id == "FEDEX"
        assert carriers[1].name == "FedEx"
        mock_client.get.assert_called_once_with("/carriers")


# Test case: get all carriers when the list is empty
def test_get_all_carriers_empty_list():
    with patch("app.services.carrier_service.client") as mock_client:
        mock_client.get.return_value = {"carriers": []}

        carriers = get_all_carriers()

        assert carriers == []
        mock_client.get.assert_called_once_with("/carriers")


# Test case: get all carriers with HTTP client exception
def test_get_all_carriers_http_client_exception():
    with patch("app.services.carrier_service.client") as mock_client:
        mock_client.get.side_effect = Exception("API failure")

        with pytest.raises(Exception) as exc_info:
            get_all_carriers()

        assert "API failure" in str(exc_info.value)
        mock_client.get.assert_called_once_with("/carriers")


# mock data for packages
mock_packages = {
    "packages": [
        {
            "tracking_id": "PKG123",
            "carrier": "UPS",
            "status": "In Transit",
            "eta": "2025-07-20T10:00:00Z",
            "last_updated": "2025-07-13T14:00:00Z",
            "current_city": "Philadelphia"
        },
        {
            "tracking_id": "PKG456",
            "carrier": "FedEx",
            "status": "Delivered",
            "eta": "2025-07-12T10:00:00Z",
            "last_updated": "2025-07-13T12:00:00Z",
            "current_city": "New York"
        }
    ]
}


# Test case: get all packages successfully
@patch("app.services.package_service.client")
def test_get_all_packages_success(mock_client):
    mock_client.get.return_value = mock_packages

    packages = get_all_packages()

    assert len(packages) == 2
    assert all(isinstance(p, Package) for p in packages)
    assert packages[0].tracking_id == "PKG123"
    mock_client.get.assert_called_once_with("/tracking")


# Test case: get all packages successfully with filters
@patch("app.services.package_service.client")
def test_get_all_packages_filter_by_status(mock_client):
    mock_client.get.return_value = mock_packages

    packages = get_all_packages(status="Delivered")

    assert len(packages) == 1
    assert packages[0].status == "Delivered"


# Test case: get all packages successfully with sorting by eta
@patch("app.services.package_service.client")
def test_get_all_packages_sort_by_eta(mock_client):
    mock_client.get.return_value = mock_packages

    packages = get_all_packages(sort_by="eta")

    assert packages[0].tracking_id == "PKG456"  # earliest ETA
    assert packages[1].tracking_id == "PKG123"


# Test case: get package by tracking ID successfully
@patch("app.services.package_service.client")
def test_get_package_by_tracking_id_found(mock_client):
    mock_client.get.return_value = mock_packages

    pkg = get_package_by_tracking_id("PKG456")

    assert isinstance(pkg, Package)
    assert pkg.tracking_id == "PKG456"
    assert pkg.carrier == "FedEx"


# Test case: get package by tracking ID not found
@patch("app.services.package_service.client")
def test_get_package_by_tracking_id_not_found(mock_client):
    mock_client.get.return_value = mock_packages

    pkg = get_package_by_tracking_id("NONEXISTENT")

    assert pkg is None


# Test case: a successful GET request
@patch("app.services.http_client.requests.get")
def test_get_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Success"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = MockApiClient(base_url="http://localhost:8080")
    result = client.get("/test-endpoint")

    mock_get.assert_called_once_with("http://localhost:8080/test-endpoint")
    assert result == {"message": "Success"}


# Test case: GET request raises HTTPError
@patch("app.services.http_client.requests.get")
def test_get_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
    mock_get.return_value = mock_response

    client = MockApiClient()

    with pytest.raises(requests.exceptions.HTTPError):
        client.get("/bad-endpoint")

    mock_get.assert_called_once_with("http://localhost:8080/bad-endpoint")


# Test case: Test default base URL
def test_default_base_url():
    client = MockApiClient()
    assert client.base_url == "http://localhost:8080"