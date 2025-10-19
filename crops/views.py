from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import FavoriteCrop
import requests
import json
import os

def home(request):
    if request.method == 'GET' and 'crop' in request.GET:
        crop_name = request.GET.get('crop').strip()
        print(f"Redirecting to crop: {crop_name}")
        return redirect('crop_price', crop_name=crop_name)
    return render(request, 'crops/home.html')

@login_required
def crop_price(request, crop_name):
    print(f"Received crop_name: {crop_name}")
    
    # Map app commodities to API Ninjas symbols
    commodity_map = {
        'wheat': 'wheat',
        'maize': 'corn',
        'rice': 'rough_rice',
        'soybeans': 'soybean_meal',
        'sugar': 'sugar',
        'coffee': 'coffee',
        'cotton': 'cotton',
        'barley': 'barley',
        'oats': 'oat',
        'feeder_cattle': 'feeder_cattle',
        'lumber': 'lumber',

    }
    api_symbol = commodity_map.get(crop_name.lower(), None)
    
    if not api_symbol:
        print(f"Invalid crop: {crop_name}")
        messages.error(request, f'Crop "{crop_name}" not supported. Try wheat, maize, rice, etc.')
        return redirect('home')

    # Mock historical data (2012–2016) for charts
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
    }
    
    # Mock data for latest price and units (updated for 2025)
    mock_data_map = {
        'wheat': {'value': 173.00, 'unit': 'USD per Metric Ton', 'year': 2025},
        'maize': {'value': 196.00, 'unit': 'USD per Metric Ton', 'year': 2025},
        'rice': {'value': 373.00, 'unit': 'USD per Metric Ton', 'year': 2025},
        'soybeans': {'value': 383.00, 'unit': 'USD per Metric Ton', 'year': 2025},
        'sugar': {'value': 0.16, 'unit': 'USD per Pound', 'year': 2025},
        'coffee': {'value': 3.96, 'unit': 'USD per Pound', 'year': 2025},
        'cotton': {'value': 0.64, 'unit': 'USD per Pound', 'year': 2025},
        'barley': {'value': 118.00, 'unit': 'USD per Metric Ton', 'year': 2025},
        'oats': {'value': 260.00, 'unit': 'USD per Metric Ton', 'year': 2025},
    }
    mock_info = mock_data_map.get(crop_name.lower(), {'value': 'N/A', 'unit': 'USD per unit', 'year': 'N/A'})

    # Prepare chart data as JSON strings
    historical = mock_historical.get(crop_name.lower(), [])
    chart_labels = json.dumps([str(item['year']) for item in historical])
    chart_prices = json.dumps([item['price'] for item in historical])

    # Try API Ninjas for live data
    API_KEY = os.environ.get('API_NINJAS_KEY', 'lhEDnNdRq9Lzp/RrpayJXQ==l9wgeT0d3TN3tnQ7')
    base_url = "https://api.api-ninjas.com/v1/commodityprice"
    headers = {'X-Api-Key': API_KEY}
    params = {'name': api_symbol}

    try:
        print(f"API URL: {base_url}?name={api_symbol}")
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        print(f"API response status: {response.status_code}")
        print(f"API response body: {response.text}")
        data = response.json()
        
        if response.status_code == 200 and 'price' in data and data.get('name'):
            live_price = data['price']
            live_unit = data.get('unit', mock_info['unit'])  # Fallback to mock unit
            context = {
                'crop': crop_name.capitalize(),
                'value': live_price,
                'unit': live_unit,
                'display_year': 'Live (2025-10-19)',
                'source': 'API Ninjas (Real-Time)',
                'chart_labels': chart_labels,
                'chart_prices': chart_prices,
            }
        else:
            print(f"API failed, response: {data}")
            messages.warning(request, f'Live data unavailable for {crop_name.capitalize()} - using mock data.')
            context = {
                'crop': crop_name.capitalize(),
                'value': mock_info['value'],
                'unit': mock_info['unit'],
                'display_year': mock_info['year'],
                'source': 'Mock Data (Updated 2025)',
                'chart_labels': chart_labels,
                'chart_prices': chart_prices,
            }
    except requests.RequestException as e:
        print(f"API error: {type(e).__name__}: {str(e)}")
        messages.warning(request, f'Live data unavailable for {crop_name.capitalize()} - using mock data.')
        context = {
            'crop': crop_name.capitalize(),
            'value': mock_info['value'],
            'unit': mock_info['unit'],
            'display_year': mock_info['year'],
            'source': 'Mock Data (Updated 2025)',
            'chart_labels': chart_labels,
            'chart_prices': chart_prices,
        }
    
    return render(request, 'crops/price.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'crops/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'crops/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = '/'

@login_required
def profile(request):
    favorites = FavoriteCrop.objects.filter(user=request.user)
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        if crop_name:
            FavoriteCrop.objects.create(user=request.user, crop_name=crop_name)
            messages.success(request, f'Added {crop_name} to favorites!')
        return redirect('profile')
    return render(request, 'crops/profile.html', {'favorites': favorites})