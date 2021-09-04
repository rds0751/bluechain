from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from level.models import UserTotal
from users.models import User
from wallets.models import WalletHistory, PaymentOption
import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = "Count Binary Data"

    def handle(self, *args, **options):
        users = UserTotal.objects.filter(active=True).order_by('user')
        for user in users:
            useru = User.objects.get(username=user)
            wallet = useru.wallet
            wallet10 = wallet*0.10
            levelp = user
            try:
                plan_ends = levelp.activated_at
                if plan_ends != 'gone' and plan_ends != 'not active':
                    date_diff = plan_ends - timezone.now() - datetime.timedelta(days=1)
                else:
                    date_diff = 'blank'
                if date_diff != 'blank':
                    total_days = levelp.level.expiration_period * 30
                    rate = levelp.level.return_amount/total_days
                    return_total = -(rate*date_diff.days)
                if return_total <= 0:
                    return_total = 0
            except Exception as e:
                raise e
            try:
                wallet = PaymentOption.objects.get(user=user)
            except Exception as e:
                wallet = 1
            if wallet != 1:
                print(str(useru)+', '+str(useru.name)+', '+str(return_total)+', '+str(wallet10)+', '+str(wallet.account_number)+', '+str(wallet.ifsc))
            else:
                print(str(useru)+', '+str(useru.name)+', '+str(return_total)+', '+str(wallet10))