import requests

BASE_URL='https://api.spot-hinta.fi'

def get_electricity_price_just_now():
    
    endpoint = f"{BASE_URL}/JustNow"
    
    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()
        return float(data["PriceWithTax"])
    else:
        return False
    
