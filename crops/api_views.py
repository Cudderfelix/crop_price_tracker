from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PriceHistory, PriceAlert
from .serializers import PriceSerializer, AlertSerializer
import requests
from django.conf import settings

class PriceViewSet(viewsets.ViewSet):
    def list(self, request):
        crop = request.query_params.get('crop')
        days = int(request.query_params.get('days', 1))
        
        if crop:
            data = PriceHistory.objects.filter(crop=crop.lower()).order_by('-date')[:days]
            return Response(PriceSerializer(data, many=True).data)
        return Response({"error": "crop parameter required"}, status=400)

    def retrieve(self, request, pk):
        # Live fetch if not in DB
        url = f"https://api.api-ninjas.com/v1/commodityprice?name={pk}"
        headers = {'X-Api-Key': settings.API_NINJAS_KEY}
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            return Response({
                "crop": pk,
                "price": data['price'],
                "unit": data.get('unit', 'USD/Unit'),
                "source": "API Ninjas (Live)"
            })
        return Response({"error": "Not found"}, status=404)

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    queryset = PriceAlert.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)