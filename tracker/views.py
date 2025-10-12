from django.shortcuts import render
import requests

def home(request):
    crop_data = None
    error = None
    if 'crop' in request.GET:
        crop_name = request.Get['crop'].lower()
        try:
            response = {
                'crop': crop_name,
                'price': 5.50,
                'unit': 'bushel',
                'date': '2025-10-10'
            }
            crop_data = response
        except Exception as e:
            error = "Error fetching data. Please try again."

    return render(request, 'tracker/home.html', {'crop_data': crop_data, 'error': error})
