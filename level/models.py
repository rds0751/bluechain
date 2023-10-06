from django.db import models
from datetime import datetime
from django.utils import timezone


class Activation(models.Model):
    user = models.CharField(max_length=25, blank=True, null=True)
    amount = models.IntegerField()
    paid_by = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    utr_number = models.CharField(max_length=255, blank=True, null=True)
    reciept_number = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to='activation/', null=True)
    status = models.CharField(max_length=8)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class LevelIncomeSettings(models.Model):  
    level = models.IntegerField()
    amount = models.IntegerField()
    name = models.CharField(max_length=125, null=True, blank=True)
    permanent_reward = models.FloatField()
    active = models.BooleanField(default=True)
    pool_roi = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class LevelUser(models.Model):
    user = models.CharField(max_length=25, blank=True, null=True)
    level = models.ForeignKey(LevelIncomeSettings, on_delete=models.CASCADE)
    active = models.BooleanField()
    direct = models.CharField(max_length=25, blank=True, null=True)
    business = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user)    

class PoolUser(models.Model):
    user = models.CharField(max_length=25, blank=True, null=True, unique=True)
    level = models.IntegerField(default=0)
    plan = models.ForeignKey(LevelIncomeSettings, null=True, on_delete=models.CASCADE)
    downlines = models.IntegerField(default=0)
    plan = models.ForeignKey(LevelIncomeSettings, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    upline = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user)