from pydantic import BaseModel, Field


class Carrier(BaseModel):
    """
    Pydantic model representing a shipping carrier.
    """
    id: str = Field(
        ...,
        description="Unique identifier for the carrier.",
        example="UPS"
    )
    name: str = Field(
        ...,
        description="Full name of the carrier.",
        example="United Parcel Service"
    )