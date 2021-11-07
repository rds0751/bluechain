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
            wallet9 = wallet - wallet*0.10*0.95
            wallet10 = wallet - wallet*0.10*0.95
            levelp = user
            start_date = datetime.datetime.now() + datetime.timedelta(-30)
            end_date = datetime.datetime.now()
            newusers = UserTotal.objects.filter(activated_at__range=(start_date, end_date))
            if user in newusers:
                wallet10 = wallet9
            try:
                plan_ends = levelp.activated_at
                if plan_ends != 'gone' and plan_ends != 'not active':
                    date_diff = plan_ends - timezone.now() - datetime.timedelta(days=1)
                else:
                    date_diff = 'blank'
                if date_diff != 'blank':
                    total_days = levelp.level.expiration_period * 30
                    rate = levelp.level.return_amount/total_days
                    if user in newusers:
                        return_total = -(rate*date_diff.days)*0.95
                    else:
                        return_total = (rate*30)*0.95
            except Exception as e:
                raise e
            try:
                wallet = PaymentOption.objects.get(user=user)
            except Exception as e:
                wallet = 1
            if wallet != 1:
                print(str(useru)+', '+str(useru.email)+', '+', '+str(useru.mobile)+', '+', '+str(useru.name)+', '+str(return_total)+', '+str(wallet10)+', "'+str(wallet.account_number)+'", '+str(wallet.ifsc))
            else:
                print(str(useru)+', '+str(useru.email)+', '+', '+str(useru.mobile)+', '+', '+str(useru.name)+', '+str(return_total)+', '+str(wallet10))

