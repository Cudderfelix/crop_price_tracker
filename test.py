import requests

key = "lhEDnNdRq9Lzp/RrpayJXQ==l9wgeT0d3TN3tnQ7"
url = "https://api.api-ninjas.com/v1/commodityprice?name=rice"

resp = requests.get(url, headers={'X-Api-Key': key})
print("Status:", resp.status_code)
print("Response:", resp.json())
