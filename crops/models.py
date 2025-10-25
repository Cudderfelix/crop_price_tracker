"""from django.db import models
from django.contrib.auth.models import User

class FavoriteCrop(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       crop_name = models.CharField(max_length=100)
       added_date = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return f"{self.user.username} - {self.crop_name}"""

from django.db import models
from django.contrib.auth.models import User

class PriceHistory(models.Model):
    crop = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(max_length=50)
    date = models.DateField()
    source = models.CharField(max_length=50, default="API Ninjas")

    class Meta:
        unique_together = ('crop', 'date')

class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.CharField(max_length=50)
    target_price = models.DecimalField(max_digits=10, decimal_places=4)
    condition = models.CharField(max_length=10, choices=[('below', 'Below'), ('above', 'Above')])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)