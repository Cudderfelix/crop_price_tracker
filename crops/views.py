from django.shortcuts import render, redirect
import requests
import json

def home(request):
       if request.method == 'GET' and 'crop' in request.GET:
           crop_name = request.GET.get('crop').strip()
           print(f"Redirecting to crop: {crop_name}")
           return redirect('crop_price', crop_name=crop_name)
       return render(request, 'crops/home.html')

def crop_price(request, crop_name):
       print(f"Received crop_name: {crop_name}")
       
       commodity_map = {
           'wheat': 'wheat',
           'maize': 'corn',
           'rice': 'rice',
           'soybeans': 'soybeans',
           'sugar': 'sugar',
           'coffee': 'coffee',
           'cotton': 'cotton',
           'barley': 'barley',
           'oats': 'oats',
       }
       commodity_name = commodity_map.get(crop_name.lower(), None)
       
       if not commodity_name:
           print(f"Invalid crop: {crop_name}")
           return render(request, 'crops/error.html', {'error': f'Crop "{crop_name}" not supported. Try wheat, maize, rice, soybeans, sugar, coffee, cotton, barley, or oats.'})

       # Mock historical data (2012–2016, realistic IMF-based)
       mock_historical = {
           'wheat': [
               {'year': 2012, 'price': 210.50},
               {'year': 2013, 'price': 195.30},
               {'year': 2014, 'price': 190.10},
               {'year': 2015, 'price': 185.00},
               {'year': 2016, 'price': 180.23},
           ],
           'maize': [
               {'year': 2012, 'price': 180.00},
               {'year': 2013, 'price': 175.50},
               {'year': 2014, 'price': 170.20},
               {'year': 2015, 'price': 168.80},
               {'year': 2016, 'price': 168.50},
           ],
           'rice': [
               {'year': 2012, 'price': 450.00},
               {'year': 2013, 'price': 440.00},
               {'year': 2014, 'price': 435.00},
               {'year': 2015, 'price': 430.00},
               {'year': 2016, 'price': 428.00},
           ],
           'soybeans': [
               {'year': 2012, 'price': 400.00},
               {'year': 2013, 'price': 390.00},
               {'year': 2014, 'price': 385.00},
               {'year': 2015, 'price': 382.00},
               {'year': 2016, 'price': 384.00},
           ],
           'sugar': [
               {'year': 2012, 'price': 0.18},
               {'year': 2013, 'price': 0.15},
               {'year': 2014, 'price': 0.14},
               {'year': 2015, 'price': 0.13},
               {'year': 2016, 'price': 0.12},
           ],
           'coffee': [
               {'year': 2012, 'price': 2.20},
               {'year': 2013, 'price': 2.10},
               {'year': 2014, 'price': 2.00},
               {'year': 2015, 'price': 1.98},   
               {'year': 2016, 'price': 1.95},
           ],
           'cotton': [
               {'year': 2012, 'price': 0.85},
               {'year': 2013, 'price': 0.80},
               {'year': 2014, 'price': 0.75},
               {'year': 2015, 'price': 0.70},               
               {'year': 2016, 'price': 0.68},
           ],        
           'barley': [
               {'year': 2012, 'price': 160.00},
               {'year': 2013, 'price': 150.00}, 
               {'year': 2014, 'price': 145.00},
               {'year': 2015, 'price': 140.00},               
               {'year': 2016, 'price': 139.00},
           ],
           'oats': [
               {'year': 2012, 'price': 190.00},
               {'year': 2013, 'price': 185.00},
               {'year': 2014, 'price': 180.00},
               {'year': 2015, 'price': 175.00},               
               {'year': 2016, 'price': 173.00},
           ],
       }
       
     
       
       mock_data_map = {
           'wheat': {'value': 180.23, 'unit': 'USD per Metric Ton', 'year': 2016},
           'maize': {'value': 168.50, 'unit': 'USD per Metric Ton', 'year': 2016},
           'rice': {'value': 428.00, 'unit': 'USD per Metric Ton', 'year': 2016},
           'soybeans': {'value': 384.00, 'unit': 'USD per Metric Ton', 'year': 2016},
           'sugar': {'value': 0.12, 'unit': 'USD per Pound', 'year': 2016},
           'coffee': {'value': 1.95, 'unit': 'USD per Pound', 'year': 2016},
           'cotton': {'value': 0.68, 'unit': 'USD per Pound', 'year': 2016},
           'barley': {'value': 139.00, 'unit': 'USD per Metric Ton', 'year': 2016},
           'oats': {'value': 173.00, 'unit': 'USD per Metric Ton', 'year': 2016},
       }
       mock_info = mock_data_map.get(crop_name.lower(), {'value': 'N/A', 'unit': 'USD per unit', 'year': 'N/A'})

       # Prepare chart data
       #historcial = mock_historical.get(crop_name.lower(), [])
       #chart_labels = [str(item['year']) for item in historical]
       #chart_prices = [item['price'] for item in historical]

         # Try Opendatasoft API
       base_url = "https://data.opendatasoft.com/api/records/1.0/search/"
       params = {
           'dataset': 'commodity-prices',
           'q': f'commodity:{commodity_name}',
           'facet': 'commodity',
           'facet': 'year',
           'rows': 1,
           'sort': '-year',
           'format': 'json'
       }

       try:
           print(f"API URL: {base_url}?{requests.compat.urlencode(params)}")
           response = requests.get(base_url, params=params, timeout=10)
           print(f"API response status: {response.status_code}")
           data = response.json()
           print(f"API response keys: {list(data.keys())}")
           
           if 'error' in data:
               print(f"API dataset error: {data['error']} - Using mock data")
               context = {
                   'crop': crop_name.capitalize(),
                   'value': mock_info['value'],
                   'unit': mock_info['unit'],
                   'year': mock_info['year'],
                   'source': 'Mock Data (Historical IMF, up to 2016)',
                   'historical_data': mock_historical.get(crop_name.lower(), [])
               }
               return render(request, 'crops/price.html', context)
           
           if data.get('records') and len(data['records']) > 0:
               latest_record = data['records'][0]
               fields = latest_record.get('fields', {})
               print(f"Latest data fields: {fields}")
               
               context = {
                   'crop': crop_name.capitalize(),
                   'value': fields.get('price_usd', mock_info['value']),
                   'unit': fields.get('price_usd_per', mock_info['unit']),
                   'year': fields.get('year', mock_info['year']),
                   'source': 'Opendatasoft (IMF Data, up to 2016)',
                   'historical_data': mock_historical.get(crop_name.lower(), [])  # Use mock for now
               }
               return render(request, 'crops/price.html', context)
           else:
               print("No records found - Using mock data")
               context = {
                   'crop': crop_name.capitalize(),
                   'value': mock_info['value'],
                   'unit': mock_info['unit'],
                   'year': mock_info['year'],
                   'source': 'Mock Data (Historical IMF, up to 2016)',
                   'historical_data': mock_historical.get(crop_name.lower(), [])
               }
               return render(request, 'crops/price.html', context)
               
       except Exception as e:
           print(f"API error (using mock fallback): {e}")
           context = {
               'crop': crop_name.capitalize(),
               'value': mock_info['value'],
               'unit': mock_info['unit'],
               'year': mock_info['year'],
               'source': 'Mock Data (Historical IMF, up to 2016) - API temporarily unavailable',
               'historical_data': mock_historical.get(crop_name.lower(), [])
           }
           return render(request, 'crops/price.html', context)