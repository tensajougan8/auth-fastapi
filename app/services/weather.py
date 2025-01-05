import requests


async def get_weather():
    response = requests.get("https://api.data.gov.sg/v1/environment/air-temperature")
    return response.json()