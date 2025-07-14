from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class SortBy(str, Enum):
    """Enum for sorting options on the /packages endpoint."""
    eta = "eta"
    last_updated = "last_updated"


class PackageStatus(str, Enum):
    """Enum for allowed package delivery statuses."""
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    OUT_FOR_DELIVERY = "Out for Delivery"


class Package(BaseModel):
    """
    Pydantic model representing a package's tracking data.
    """
    tracking_id: str = Field(
        ...,
        description="Unique identifier for the package.",
        example="PKG123456"
    )
    carrier: str = Field(
        ...,
        description="Name of the carrier handling the package.",
        example="UPS"
    )
    status: PackageStatus = Field(
        ...,
        description="Current delivery status of the package.",
        example="In Transit"
    )
    eta: datetime = Field(
        ...,
        description="Estimated time of arrival for the package."
    )
    last_updated: datetime = Field(
        ...,
        description="Last updated timestamp for the package status."
    )
    current_city: str = Field(
        ...,
        description="Current city where the package is located.",
        example="Philadelphia"
    )
