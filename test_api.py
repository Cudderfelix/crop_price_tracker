import requests

url = "http://fenixservices.fao.org/faostat/api/v1/en/data/FPI"
params = {
    'area': 1,  # World
    'item': 15,  # Wheat
    'year': 2024,
    'limit': 1,
    'offset': 0,
    'dissemination_format': 'json'
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
