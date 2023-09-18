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
		
		levels = {
            'level1': 75/100,
            'level2': 10/100,
            'level3': 10/100,
            'level4': 5/100,
            'level5': 5/100,
            'level6': 4/100,
            'level7': 4/100,
            'level8': 4/100,
            'level9': 4/100,
            'level10': 4/100,
            'level11': 3/100,
            'level12': 3/100,
            'level13': 3/100,
            'level14': 3/100,
            'level15': 3/100,
            'level16': 2/100,
            'level17': 2/100,
            'level18': 2/100,
            'level19': 2/100,
            'level20': 2/100
			}

		for x in l:
			directs = LevelUser.objects.filter(direct=x.user).count()
			time_difference = timezone.now() - x.activated_at
			days_difference = time_difference.days
			roi = x.level.amount * 0.005 + x.level.amount * 0.005 * 0.01 * directs
			count = 0
			for d in range(0,days_difference):
				wallet = WalletHistory()
				wallet.comment = "Profit Share Income"
				wallet.user_id = x.user
				wallet.amount = roi
				wallet.type = "credit"
				wallet.created_at = timezone.now() - timedelta(days=count)
				wallet.save()
				user = User.objects.get(username=x.user)
				user.wallet += roi
				user.save()
				userid = User.objects.get(username=user.username)
				level = 0
				upline_user = userid.referral 
				userid = user
				amount = x.level.amount * 0.05 / 30
				uplines = [upline_user, ]
				count += 1
				print(days_difference, count)