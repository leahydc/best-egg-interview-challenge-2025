from pydantic import BaseModel
from datetime import datetime

# Pydantic Package model for data validation
class Package(BaseModel):
    tracking_id: str
    carrier: str
    status: str
    eta: datetime
    last_updated: datetime
    current_city: str