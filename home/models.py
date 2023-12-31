from django.db import models
from django.conf import settings
from level.models import LevelUser
# Create your models here.
class Device(models.Model):
	devicename = models.CharField(max_length=200, null=True, blank=True)
	deviceid = models.CharField(max_length=200, null=True, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return 'Device: '+self.deviceid

class Message(models.Model):
    message = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=25, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
    	return self.message

class News(models.Model):
	news = models.TextField()
	type = models.CharField(max_length=50)

	def __str__(self):
		return self.news
	
class Company(models.Model):
	total_turnover = models.FloatField()
	today_turnover = models.FloatField()
	today_new_ids = models.FloatField()

	def total_active_ids(self):
		c = LevelUser.objects.filter(active=True).count()
		return c