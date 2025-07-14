import requests

# HTTP Client to interact with a mock API and fetch data from the mock server
class MockApiClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url

    def get(self, path: str):
        url = f"{self.base_url}{path}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()