from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistory
import datetime
from datetime import timedelta
from level.models import LevelIncomeSettings, LevelUser
from users.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from home.models import Company


class Command(BaseCommand):
	help = "Send ROI Incomes"

	def handle(self, *args, **options):
		l = LevelUser.objects.filter(level__amount__gte=20)
		
		def generateid():
			txnid = get_random_string(8)
			try:
				txn = WalletHistory.objects.get(txnid = txnid)
			except WalletHistory.DoesNotExist:
				txn = 0
			if txn:
				generateid()
			else:
				return txnid
			
		def finduplines(user):  
			try:
				user = User.objects.get(username__iexact=str(user))
				upline = user.referral   
			except User.DoesNotExist:   
				upline = 'blank'
			return upline
		
		l = LevelUser.objects.filter(active=True)
		c = Company.objects.get(id=1)
		amount = c.today_turnover
		amount = (amount / l.count()) * 0.4
		for x in l:
			if User.objects.get(username=x.user).total_income + amount <= 2 * 100: 
				wallet = WalletHistory()
				wallet.comment = "Global Community Income"
				wallet.user_id = x.user
				wallet.amount = amount
				wallet.type = "credit"
				wallet.created_at = timezone.now()
				wallet.save()
				user = User.objects.get(username=x.user)
				user.today_income = 0
				user.save()
				user = User.objects.get(username=x.user)
				user.wallet += amount
				user.total_income += amount
				user.today_income += amount
				user.global_income += amount
				user.save()
				c.today_new_ids = 0
				c.today_turnover = 0
				c.save()
