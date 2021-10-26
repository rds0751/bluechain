from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistory
import datetime

class Command(BaseCommand):
	help = "Count Binary Data"

	def handle(self, *args, **options):
		start_date = datetime.datetime.now() + datetime.timedelta(-100)
		end_date = datetime.datetime.now() + datetime.timedelta(-15)
		w = WalletHistory.objects.filter(created_at__range=(start_date, end_date), comment__icontains="New Upgrade by").exclude(filter__icontains="payment done")
		for x in w:
			try:
				user = User.objects.get(username=x.user_id)
			except Exception as e:
				user = 'blank'
			if user != 'blank':
				user.wallet += x.amount
				user.save()
				x.filter = 'payment done'
				x.save()