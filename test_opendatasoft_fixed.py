import requests

base_url = "https://data.opendatasoft.com/api/records/1.0/search/"
params = {
    'dataset': 'commodity-prices',
    'q': 'commodity:wheat',
    'rows': 1,
    'sort': '-year',
    'format': 'json'
}

try:
    response = requests.get(base_url, params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")