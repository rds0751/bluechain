from django.contrib import admin

# Register your models here.
from .models import Device, Message, News, Company


admin.site.register(Device)
admin.site.register(Message)
admin.site.register(News)
admin.site.register(Company)