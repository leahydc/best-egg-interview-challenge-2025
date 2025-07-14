from typing import List
from app.models.carrier import Carrier
from app.services.http_client import MockApiClient

client = MockApiClient()


def get_all_carriers() -> List[Carrier]:
    """
    Fetch a list of all carriers from the mock API.

    Returns:
        List[Carrier]: A list of Carrier objects parsed from the API response.

    Raises:
        ValueError: If the API response is malformed or missing expected data.
    """
    response = client.get("/carriers")
    carriers = response.get("carriers")

    if carriers is None:
        raise ValueError("Missing 'carriers' field in response from mock API")

    return [Carrier(id=item["id"], name=item["name"]) for item in carriers]
