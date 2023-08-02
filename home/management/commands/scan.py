# from django.core.management.base import BaseCommand
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import json
# from users.models import User
# from wallets.models import WalletHistory
# from level.models import LevelIncomeSettings, PoolUser
# import datetime
# from django.utils.crypto import get_random_string

# class Command(BaseCommand):
# 	help = "Count Binary Data"

# 	def handle(self, *args, **options):
# 		def generateid():
# 			txnid = get_random_string(8)
# 			try:
# 				txn = WalletHistory.objects.get(txnid = txnid)
# 			except WalletHistory.DoesNotExist:
# 				txn = 0
# 			if txn:
# 				generateid()
# 			else:
# 				return txnid

# 		p = PoolUser.objects.all()
# 		for x in p:
# 			try:
# 				user = User.objects.get(username=x.user)
# 			except Exception as e:
# 				user = 'blank'

# 			today = datetime.datetime.now().date()
# 			created = x.created_at.date()

# 			print(today, created, today.day - created.day)
# 			dif = today.day - created.day
# 			roi = x.plan.pool_roi
# 			amount = x.plan.amount * roi / 100
# 			print(amount)
# 			for x in range(0, dif):
# 				upline_wallet = WalletHistory()
# 				upline_wallet.user_id = user
# 				upline_wallet.amount = amount
# 				upline_wallet.type = "credit"
# 				upline_wallet.comment = "1st Pair Income"
# 				upline_wallet.balance += amount
# 				upline_wallet.txnid = generateid()
# 				upline_wallet.save()
# 				user.wallet += amount
# 				user.today_income += amount
# 				user.total_income += amount
# 				user.progress += amount
# 				user.save()