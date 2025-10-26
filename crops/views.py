import os
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import FavoriteCrop
from django.http import JsonResponse
import requests
import json

# AUTH & HOME
def home(request):
    if request.method == 'GET' and 'crop' in request.GET:
        crop_name = request.GET.get('crop').strip()
        return redirect('crop_price', crop_name=crop_name)
    return render(request, 'crops/home.html')

@login_required
def crop_price(request, crop_name):
    print(f"Received crop_name: {crop_name}")
    
    # Map app commodities to API Ninjas symbols
    commodity_map = {
        'rice': 'rough_rice',
        'soybeans': 'soybean_meal',
        'oats': 'oat',
        'feeder_cattle': 'feeder_cattle',
        'lumber': 'lumber',
        'sugar': 'sugar',
        'coffee': 'coffee',
        'cotton': 'cotton',
        'barley': 'barley', 
        'wheat': 'wheat',
        'maize': 'corn',
    }
    api_symbol = commodity_map.get(crop_name.lower(), None)
    
    if not api_symbol:
        print(f"Invalid crop: {crop_name}")
        messages.error(request, f'Crop "{crop_name}" not supported.')
        return redirect('home')

    # Mock data fallback
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

    # Historical mock data
    mock_historical = {
        'wheat': [ ... ],
        'maize': [ ... ],
        'rice': [ ... ],
    }
    historical = mock_historical.get(crop_name.lower(), [])
    chart_labels = json.dumps([str(item['year']) for item in historical])
    chart_prices = json.dumps([item['price'] for item in historical])

    # Try API
    API_KEY = os.getenv('API_NINJAS_KEY')
    if not API_KEY:
        messages.warning(request, "API key missing. Using mock data.")
        context = {
            'crop': crop_name.capitalize(),
            'value': mock_info['value'],
            'unit': mock_info['unit'],
            'display_year': mock_info['year'],
            'source': 'Mock Data (No API Key)',
            'chart_labels': chart_labels,
            'chart_prices': chart_prices,
        }
        return render(request, 'crops/price.html', context)

    try:
        response = requests.get(
            "https://api.api-ninjas.com/v1/commodityprice",
            params={'name': api_symbol},
            headers={'X-Api-Key': API_KEY},
            timeout=10
        )
        data = response.json()

        if response.status_code == 200 and 'price' in data:
            context = {
                'crop': crop_name.capitalize(),
                'value': data['price'],
                'unit': data.get('unit', mock_info['unit']),
                'display_year': 'Live',
                'source': 'API Ninjas (Live)',
                'chart_labels': chart_labels,
                'chart_prices': chart_prices,
            }
        else:
            messages.warning(request, f"Live data unavailable: {data.get('error', 'Unknown error')}")
            context = {
                'crop': crop_name.capitalize(),
                'value': mock_info['value'],
                'unit': mock_info['unit'],
                'display_year': mock_info['year'],
                'source': 'Mock Data (API Failed)',
                'chart_labels': chart_labels,
                'chart_prices': chart_prices,
            }
        return render(request, 'crops/price.html', context)

    except requests.RequestException as e:
        messages.warning(request, f"Connection error: {str(e)}. Using mock data.")
        context = {
            'crop': crop_name.capitalize(),
            'value': mock_info['value'],
            'unit': mock_info['unit'],
            'display_year': mock_info['year'],
            'source': 'Mock Data (Connection Failed)',
            'chart_labels': chart_labels,
            'chart_prices': chart_prices,
        }
        return render(request, 'crops/price.html', context)

    # ← FINAL FALLBACK (in case of any weird case)
    return render(request, 'crops/price.html', {
        'crop': crop_name.capitalize(),
        'value': 'N/A',
        'unit': 'Error',
        'display_year': 'N/A',
        'source': 'Error',
        'chart_labels': '[]',
        'chart_prices': '[]',
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
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

# API ENDPOINTS (FREE COMMODITIES FROM API NINJAS)
def health(request):
    return JsonResponse({
        "status": "ok",
        "message": "Crop Price API is live!",
        "free_commodities": ["platinum", "oat", "rough_rice", "micro_gold"],
        "endpoints": [
            "/api/platinum/",
            "/api/oat/",
            "/api/rough-rice/",
            "/api/micro-gold/"
        ]
    })

def get_price_endpoint(request, crop):
    crop = crop.lower()
    if crop not in ['platinum', 'oat', 'rough_rice', 'micro_gold']:
        return JsonResponse({"error": "Free: platinum, oat, rough_rice, micro_gold"}, status=400)

    API_KEY = os.getenv('API_NINJAS_KEY')  # Use env var
    if not API_KEY:
        return JsonResponse({"error": "API key missing"}, status=500)

    try:
        resp = requests.get(
            "https://api.api-ninjas.com/v1/commodityprice",
            params={'name': crop},
            headers={'X-Api-Key': API_KEY},
            timeout=10
        )
        data = resp.json()
        
        if resp.status_code == 200 and 'price' in data:
            return JsonResponse({
                "crop": crop,
                "price": data['price'],
                "unit": data.get('unit', 'USD'),
                "source": "API Ninjas (Free Tier)"
            })
        else:
            return JsonResponse({"error": data.get('error', 'API error')}, status=400)
            
    except Exception as e:
        return JsonResponse({"error": f"Request failed: {str(e)}"}, status=500)
    
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def submit_price(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Use POST"}, status=405)

    try:
        data = json.loads(request.body)
        crop = data.get('crop', '').lower()
        price = data.get('price')

        if crop not in ['platinum', 'oat', 'rough_rice', 'micro_gold']:
            return JsonResponse({"error": "Invalid crop"}, status=400)
        if not price or not isinstance(price, (int, float)):
            return JsonResponse({"error": "Invalid price"}, status=400)

        # Save to DB (create model later) or just return
        return JsonResponse({
            "message": "Price submitted!",
            "crop": crop,
            "price": price,
            "status": "pending_review"
        })
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)