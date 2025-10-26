from django.db import models
from django.contrib.auth.models import User

class FavoriteCrop(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       crop_name = models.CharField(max_length=100)
       added_date = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return f"{self.user.username} - {self.crop_name}"


class PriceCache(models.Model):
    crop = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crop}: {self.price}"