from django.db import models
from datetime import datetime

# Create your models here.
class Activation(models.Model):
    user = models.CharField(max_length=25, blank=True, null=True)
    amount = models.IntegerField()
    paid_by = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    utr_number = models.CharField(max_length=255, blank=True, null=True)
    reciept_number = models.CharField(max_length=255, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

class LevelIncomeSettings(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()
    direct_commission_percentage = models.IntegerField()
    expiration_period = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

class UserTotal(models.Model):
    user = models.CharField(max_length=25, blank=True, null=True)
    level = models.IntegerField()
    active = models.BooleanField()
    left_months = models.IntegerField()
    direct = models.CharField(max_length=25, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)