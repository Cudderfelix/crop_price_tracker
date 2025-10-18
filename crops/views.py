from django.shortcuts import render, redirect
import requests

def home(request):
    if request.method == 'GET' and 'crop' in request.GET:
        crop_name = request.GET.get('crop').strip()
        return redirect ('crop_price', crop_name=crop_name)
    return render(request, 'crops/home.html')

def crop_price(request, crop_name):
       # Map crop names to FAO item codes (simplified for demo)
       crop_codes = {
           'wheat': 15,
           'maize': 56,
           'rice': 27,
       }
       item_code = crop_codes.get(crop_name.lower(), None)
       
       if not item_code:
           return render(request, 'crops/error.html', {'error': f'Crop "{crop_name}" not supported. Try wheat, maize, or rice.'})

       # FAO API request
       url = "http://fenixservices.fao.org/faostat/api/v1/en/data/FPI"
       params = {
           'area': 1,  # World
           'item': item_code,
           'year': 2024,  # Latest year
           'limit': 1,  # Latest record
           'offset': 0,
           'dissemination_format': 'json'
       }

       try:
           response = requests.get(url, params=params)
           response.raise_for_status()
           data = response.json()
           
           if data.get('data'):
               latest = data['data'][0]  # Latest entry
               context = {
                   'crop': crop_name.capitalize(),
                   'value': latest.get('Value', 'N/A'),
                   'unit': 'Price Index',  # FPI uses indices
                   'year': latest.get('Year', 'N/A'),
                   'month': latest.get('Month', 'N/A'),
                   'source': 'FAO FAOSTAT'
               }
               return render(request, 'crops/price.html', context)
           else:
               return render(request, 'crops/error.html', {'error': f'No data found for {crop_name}.'})
       except requests.exceptions.RequestException as e:
           return render(request, 'crops/error.html', {'error': f'API error: {str(e)}'})