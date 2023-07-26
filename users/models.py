from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.utils.html import mark_safe
from level.models import PoolUser


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=25, blank=True, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, default=False)
    rank = models.CharField(max_length=44, null=True, blank=True)
    profile_pic = models.FileField(upload_to='profile_pics/', null=True)
    otp = models.IntegerField(default='1234', null=True)
    referral = models.CharField(max_length=25, blank=True, null=True)
    wallet = models.FloatField(default=0)
    pool_wallet = models.FloatField(default=0)
    c = models.FloatField(default=0)
    withdrawal = models.FloatField(default=0, null=True, blank=True)
    traditional_withdrawal = models.FloatField(default=0)
    my_team = models.IntegerField(default=0)
    my_directs = models.IntegerField(default=0)
    today_income = models.FloatField(default=0)
    total_business = models.FloatField(default=0)
    sponsor_income = models.FloatField(default=0) #bahut moti 5%
    autopool_income = models.FloatField(default=0)
    rewards = models.FloatField(default=0)
    lifetime_royalty = models.FloatField(default=0)
    team_club_income = models.FloatField(default=0)
    total_income = models.FloatField(default=0)
    my_package = models.CharField(max_length=100, default='Inactive') 
    my_rank = models.CharField(max_length=100, default='Inactive')
    my_achievement = models.CharField(max_length=100, default='NA')
    progress = models.FloatField(default=0)

    
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['name', 'referal', 'mobile']
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.name:
            return self.name
        
    def my_daily_roi(self):
        try:
            p = PoolUser.objects.get(user=self.username)
        except Exception as e:
            p = 'blank'
        if p != 'blank':
            amount = p.plan.pool_roi * p.plan.amount / 100
        else:
            amount = 0
        return amount
