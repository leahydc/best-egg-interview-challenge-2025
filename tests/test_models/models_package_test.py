import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.carrier import Carrier
from app.models.package import Package

# Test cases for Carrier model validation and functionality


# Test case: valid Carrier model
def test_valid_carrier_model():
    carrier = Carrier(id="UPS", name="United Parcel Service")
    assert carrier.id == "UPS"
    assert carrier.name == "United Parcel Service"


# Test case: missing id field
def test_missing_id_field():
    with pytest.raises(ValidationError) as exc_info:
        Carrier(name="FedEx")
    errors = exc_info.value.errors()
    assert any(error["loc"] == ("id",) and error["type"] == "missing" for error in errors)


# Test case: missing name field
def test_missing_name_field():
    with pytest.raises(ValidationError) as exc_info:
        Carrier(id="FEDEX")
    errors = exc_info.value.errors()
    assert any(error["loc"] == ("name",) and error["type"] == "missing" for error in errors)


# Test case: invalid id type
def test_invalid_id_type():
    with pytest.raises(ValidationError) as exc_info:
        Carrier(id=123, name="FedEx")  # id should be a string
    errors = exc_info.value.errors()
    assert any(error["loc"] == ("id",) and error["type"].startswith("string_type") for error in errors)


# Test case: invalid name type
def test_invalid_name_type():
    with pytest.raises(ValidationError) as exc_info:
        Carrier(id="FEDEX", name=456)  # name should be a string
    errors = exc_info.value.errors()
    assert any(error["loc"] == ("name",) and error["type"].startswith("string_type") for error in errors)



# Test cases for Package model validation and functionality


# Test case: valid Package model
def test_valid_package_model():
    package = Package(
        tracking_id="PKG123456",
        carrier="UPS",
        status="In Transit",
        eta="2025-07-20T12:00:00",
        last_updated="2025-07-13T15:30:00",
        current_city="Philadelphia"
    )
    assert package.tracking_id == "PKG123456"
    assert package.carrier == "UPS"
    assert package.status == "In Transit"
    assert isinstance(package.eta, datetime)
    assert isinstance(package.last_updated, datetime)
    assert package.current_city == "Philadelphia"

# Valid data for testing each data element in Package model
valid_data = {
    "tracking_id": "PKG123456",
    "carrier": "UPS",
    "status": "In Transit",
    "eta": "2025-07-20T12:00:00",
    "last_updated": "2025-07-13T15:30:00",
    "current_city": "Philadelphia"
}


# Test case: missing tracking_id
def test_missing_tracking_id():
    data = valid_data.copy()
    del data["tracking_id"]
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "tracking_id" in str(exc_info.value)


# Test case: invalid tracking_id type
def test_invalid_tracking_id_type():
    data = valid_data.copy()
    data["tracking_id"] = 12345
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "tracking_id" in str(exc_info.value)


# Test case: missing carrier
def test_missing_carrier():
    data = valid_data.copy()
    del data["carrier"]
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "carrier" in str(exc_info.value)


# Test case: invalid carrier type
def test_invalid_carrier_type():
    data = valid_data.copy()
    data["carrier"] = {"name": "UPS"}
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "carrier" in str(exc_info.value)


# Test case: missing status
def test_missing_status():
    data = valid_data.copy()
    del data["status"]
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "status" in str(exc_info.value)


# Test case: invalid status type
def test_invalid_status_type():
    data = valid_data.copy()
    data["status"] = 404
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "status" in str(exc_info.value)


# Test case: missing eta
def test_missing_eta():
    data = valid_data.copy()
    del data["eta"]
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "eta" in str(exc_info.value)


# Test case: invalid eta format
def test_invalid_eta_format():
    data = valid_data.copy()
    data["eta"] = "not-a-date"
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "eta" in str(exc_info.value)


# Test case: missing last_updated
def test_missing_last_updated():
    data = valid_data.copy()
    del data["last_updated"]
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "last_updated" in str(exc_info.value)


# Test case: invalid last_updated format
def test_invalid_last_updated_type():
    data = valid_data.copy()
    data["last_updated"] = "not-a-date"
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "last_updated" in str(exc_info.value)


# Use case: missing current_city
def test_missing_current_city():
    data = valid_data.copy()
    del data["current_city"]
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "current_city" in str(exc_info.value)


# Test case: invalid current_city type
def test_invalid_current_city_type():
    data = valid_data.copy()
    data["current_city"] = False
    with pytest.raises(ValidationError) as exc_info:
        Package(**data)
    assert "current_city" in str(exc_info.value)