import requests
from retry import retry


@retry()
def get_location_by_ip(ip: str) -> str:
    url = f"https://ip2c.org/{ip}"
    response = requests.get(url)
    location = response.text.split(";")[-1]
    return location
