from rest_framework import serializers
from .models import PriceHistory, PriceAlert

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['crop', 'price', 'unit', 'date', 'source']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlert
        fields = ['id', 'crop', 'target_price', 'condition', 'active']