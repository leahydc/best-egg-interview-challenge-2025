from pydantic import BaseModel

# Pydantic Carrier model for data validation
class Carrier(BaseModel):
    id: str
    name: str