from django.db import models
from base.models import TimeStampedModel

class Customer(TimeStampedModel):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=255)
    AREA_CHOICES = [
        ("urban", "Urban"),
        ("suburban", "Suburban"),
        ("vip", "VIP"),
    ]
    area = models.CharField(max_length=10, choices=AREA_CHOICES)

    class Meta:
        db_table = "hr_customer"

class ServiceType(TimeStampedModel):
    name = models.CharField(max_length=100)
    price_per_m2 = models.IntegerField()
    cleaning_rate_m2_per_h = models.IntegerField()

    class Meta:
        db_table = "hr_service_type"
