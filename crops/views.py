from django.shortcuts import HttpResponse, JsonResponse
from django.shortcuts import render
import requests

def home(request):
    return HttpResponse("Hello, welcome to Cudderfelix Crop Tracker app!")

def crop_price(request, crop_name):
    # Normalize crop name (e.g., 'wheat' -> FAO item code logic)
    # Fordemo: Use FAO's food price index endpoint (simplified for wheat-like data)
    url = "http://fenixservices.fao.org/faostat/api/v1/en/data/FPI"  # For Food Price Indez
    params = {
        'area': 1, # World
        'item': 15 if crop_name.loweer() == 'wheat' else 56, # Wheat-15, Maize=56 (adjust as needed)
        'year': 2024, # Current year
        'limit': 10,
        'offset': 0,
        'dissemination_format': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise error for a bad server status
        data = response.json()

        # Simple parsing: Extract latest price/index
        if data.get('data'):
            latest = data['data'][-1] # Last entry
            price_info = {
                'crop': crop_name.capitalize(),
                'value': latest.get('value', 'N/A'),
                'unit': latest.get('Element', 'Index'), # Latest Price Index
                'year': latest.get('Year', 'N/A'),
                'source': 'FAO FAOSTAT'
            }
            return JsonResponse(price_info) # For now, return JSON; we'll add templates next
        else:
            return HttpResponse(f"No data found for {crop_name}.", status=404)
    except requests.exceptions.RequestExxception as e:
        return HttpResponse(f"API error: {str(e)}", status=500)
