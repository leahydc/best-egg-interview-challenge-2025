from pydantic import BaseModel, Field

# Pydantic Carrier model for data validation
class Carrier(BaseModel):
    id: str = Field(..., description="Unique identifier for the carrier")
    name: str = Field(..., description="Name of the carrier")