from pydantic import BaseModel, Field
from app.models.package import Package


class CityMetadata(BaseModel):
    """
    Metadata about a city where a package is currently located.
    """
    city: str = Field(
        ...,
        description="Name of the city.",
        example="Philadelphia"
    )
    state: str = Field(
        ...,
        description="Two-letter state code where the city is located.",
        example="PA"
    )
    timezone: str = Field(
        ...,
        description="Timezone of the city.",
        example="EST"
    )
    lat: float = Field(
        ...,
        description="Latitude of the city.",
        example=39.9526
    )
    lon: float = Field(
        ...,
        description="Longitude of the city.",
        example=-75.1652
    )


class EnrichedPackage(BaseModel):
    """
    A package enriched with city-level metadata from its current location.
    """
    package: Package = Field(
        ...,
        description="The package object containing tracking details."
    )
    city_metadata: CityMetadata = Field(
        ...,
        description="Metadata about the city where the package is currently located."
    )
