from typing import List
from app.models.carrier import Carrier
from app.services.http_client import MockApiClient

client = MockApiClient()

# Function to provide a list of all carriers from the mock API
def get_all_carriers() -> List[Carrier]:
    carriers_data = client.get("/carriers")
    carrier_list = carriers_data.get("carriers", [])  # Extract the actual list
    return [Carrier(id=item["id"], name=item["name"]) for item in carrier_list]