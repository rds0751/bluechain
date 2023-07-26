from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistory
from level.models import LevelIncomeSettings, PoolUser
import datetime

class Command(BaseCommand):
	help = "Count Binary Data"

	def handle(self, *args, **options):

		p = PoolUser.objects.all()
		for x in p:
			try:
				user = User.objects.get(username=x.user)
			except Exception as e:
				user = 'blank'

			today = datetime.datetime.now().date()
			created = x.created_at.date()

			print(today, created, today.day - created.day)
			dif = today.day - created.day
			roi = x.plan.pool_roi
			amount = x.plan.amount * roi / 100
			print(amount)
			for x in range(0, dif):
				