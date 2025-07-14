from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# ENUM values for sorting packages to validate request
class SortBy(str, Enum):
    eta = "eta"
    last_updated = "last_updated"

# ENUM values for package status to validate request
class PackageStatus(str, Enum):
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    OUT_FOR_DELIVERY = "Out for Delivery"

# Pydantic Package model for data validation
class Package(BaseModel):
    tracking_id: str = Field(..., description="Unique identifier for the package")
    carrier: str = Field(..., description="Name of the carrier handling the package")
    status: str = Field(..., description="Current status of the package", example="In Transit")
    eta: datetime = Field(..., description="Estimated time of arrival for the package")
    last_updated: datetime = Field(..., description="Last updated timestamp for the package status")
    current_city: str = Field(..., description="Current city where the package is located")