from pydantic import BaseModel
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
    tracking_id: str
    carrier: str
    status: str
    eta: datetime
    last_updated: datetime
    current_city: str