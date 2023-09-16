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
		l = LevelUser.objects.filter(active=True)
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
			time_difference = timezone.now() - x.created_at
			days_difference = time_difference.days
			roi = x.level.amount * 0.05 / 30
			wallet = WalletHistory()
			wallet.comment = "Staking Incentive"
			wallet.user_id = x.user
			wallet.amount = roi
			wallet.type = "credit"
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
			while level < 20 and upline_user != 'blank':
				upline_user = finduplines(str(upline_user))
				uplines.append(upline_user)
				level += 1


			level = 0
			for upline in uplines:
				try:
					upline_user = User.objects.get(username=upline) 
				except Exception as e:  
					upline_user = 'blank'
				try:
					upgraded = LevelUser.objects.get(user=upline, active=True)
				except Exception as e:
					upgraded = 'blank'
				if upline_user != 'blank' and upgraded != 'blank':  
					directs = LevelUser.objects.filter(direct=upline_user, active=True)
					if user.referral == upline_user.username:
						direct = True
					else:
						direct = False
					upline_amount = levels['level{}'.format(level+1)]*amount
					print(directs.count(), level, direct, days_difference)
					if directs.count() >= level / 2:
						upline_wallet = WalletHistory()   
						upline_wallet.user_id = upline  
						upline_wallet.amount = upline_amount    
						upline_wallet.type = "credit"   
						upline_wallet.comment = "New ROI by {} in level {}".format(user, level+1)
						upline_wallet.txnid = generateid()
						upline_user.wallet += upline_amount
						upline_wallet.save()
						upline_user.save()
						print('if')
					else:
						upline_wallet = WalletHistory()
						upline_wallet.user_id = upline
						upline_wallet.amount = upline_amount
						upline_wallet.type = "credit"
						upline_wallet.comment = "{} ROI but Level {} not opened!".format(user, level+1)
						upline_wallet.txnid = generateid()
						upline_wallet.save()
						print('else')
				level += 1

			print(user, wallet.amount)