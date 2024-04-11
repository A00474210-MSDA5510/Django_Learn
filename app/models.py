from django.db import models

# Create your models here.
class Hotels(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    availability = models.BooleanField(default=False)