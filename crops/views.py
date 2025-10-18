from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login  # Avoid name conflict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import SignupForm, LoginForm
import requests
import json

def home(request):
    if request.method == 'GET' and 'crop' in request.GET:
        crop_name = request.GET.get('crop').strip()
        print(f"Redirecting to crop: {crop_name}")
        return redirect('crop_price', crop_name=crop_name)
    return render(request, 'crops/home.html')

@login_required  # Protect: Users must log in to view crop prices
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
        messages.error(request, f'Crop "{crop_name}" not supported. Try wheat, maize, rice, etc.')
        return redirect('home')

    # Mock historical data (2012–2016)
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
    
    # Mock data for latest price
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

    # Prepare chart data as JSON strings
    historical = mock_historical.get(crop_name.lower(), [])
    chart_labels = json.dumps([str(item['year']) for item in historical])
    chart_prices = json.dumps([item['price'] for item in historical])

    # Try Opendatasoft API (fallback to mock)
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
        
        if 'error' in data or not data.get('records'):
            print("Using mock data")
            context = {
                'crop': crop_name.capitalize(),
                'value': mock_info['value'],
                'unit': mock_info['unit'],
                'display_year': mock_info['year'],
                'source': 'Mock Data (Historical IMF, up to 2016)',
                'chart_labels': chart_labels,
                'chart_prices': chart_prices,
            }
            return render(request, 'crops/price.html', context)
        
        # If API succeeds
        latest_record = data['records'][0]
        fields = latest_record.get('fields', {})
        context = {
            'crop': crop_name.capitalize(),
            'value': fields.get('price_usd', mock_info['value']),
            'unit': fields.get('price_usd_per', mock_info['unit']),
            'display_year': fields.get('year', mock_info['year']),
            'source': 'Opendatasoft (IMF Data)',
            'chart_labels': chart_labels,
            'chart_prices': chart_prices,
        }
        return render(request, 'crops/price.html', context)
        
    except Exception as e:
        print(f"API fallback: {e}")
        context = {
            'crop': crop_name.capitalize(),
            'value': mock_info['value'],
            'unit': mock_info['unit'],
            'display_year': mock_info['year'],
            'source': 'Mock Data (Historical IMF)',
            'chart_labels': chart_labels,
            'chart_prices': chart_prices,
        }
        return render(request, 'crops/price.html', context)

# Custom signup view
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

# Use Django's built-in LoginView (custom template)
class CustomLoginView(LoginView):
    template_name = 'crops/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

# Use Django's built-in LogoutView
class CustomLogoutView(LogoutView):
    next_page = '/'