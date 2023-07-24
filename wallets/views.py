from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView, CreateView
from django.shortcuts import render, redirect
from users.models import User
from .models import PaymentOption, Withdrawal
from wallets.models import WalletHistory, Beneficiary, MetatraderAccount, Mtw
from django.shortcuts import render
import requests
import os
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import jwt
from django.utils import timezone
from random import randint
import datetime
from level.models import LevelUser

from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import math
import random

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

def send_otp(request):
     email=request.GET.get("email")
     print(email)
     o=generateOTP()
     print(o)
     htmlgen = '<p>Your OTP is <strong>o</strong></p>'
     send_mail('OTP request',o,'<your gmail id>',[email], fail_silently=False, html_message=htmlgen)
     return HttpResponse(o)

class SearchListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "wallets/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        form = BinaryJoinForm()
        context["hide_search"] = True
        context["users_list"] = (
            get_user_model()
            .objects.filter(Q(username=query))
            .distinct()
        )
        context["form"] = form
        
        return context

@login_required
def transfer(request):
    message = ""
    amount = 0
    def generateid():
        txnid = get_random_string(8)
        try:
            txn = Recharges.objects.get(transaction_id = txnid)
        except Recharges.DoesNotExist:
            txn = 0
        if txn:
            generateid()
        else:
            return 'JR{}'.format(txnid)

    def userbal(user):
        userid = User.objects.get(username=user)
        bal = userid.income + userid.binary_income + userid.added_amount + userid.received_amount + userid.new_funds
        return bal

    ben = 'blank'
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        bene_id = request.POST.get('bene_id')
        user = request.POST.get('user_id')
        txnid = generateid()
        try:
            ben = User.objects.get(username=bene_id)
        except User.DoesNotExist:
            ben = 'blank'

    userbal = userbal(str(request.user))
    

    if ben != 'blank':
        if userbal >= amount:
            user_id = request.user
            if user_id.new_funds <= amount:
                amount = amount - user_id.new_funds
                user_id.new_funds = 0
                if user_id.income <= amount:
                    amount = amount - user_id.income
                    user_id.income = 0
                    print("if1")
                    if user_id.binary_income <= amount:
                        amount = amount - user_id.binary_income
                        user_id.binary_income = 0
                        print("if2")
                        if user_id.added_amount <= amount:
                            amount = amount - user_id.added_amount
                            user_id.added_amount = 0
                            print("if3")
                            if amount != 0:
                                user_id.received_amount = user_id.received_amount - amount
                                amount = 0
                                print("if4")
                        else:
                            user_id.added_amount = user_id.added_amount - amount
                            amount = 0
                            print("if5")
                    else:
                        user_id.binary_income = user_id.binary_income - amount
                        amount = 0
                        print("if6")
                else:
                    user_id.income = user_id.income - amount
                    amount = 0
            else:
                user_id.new_funds = user_id.new_funds - amount
                amount = 0
                
            user_id.save()
            if request.method == 'POST':
                status = 'success'
                amount = float(request.POST.get('amount'))
                if status == 'success':
                    userwallet = WalletHistory()
                    userwallet.user_id = str(user_id)
                    userwallet.amount = float(amount)
                    userwallet.type = "debit"
                    userwallet.comment = "sent to {}".format(str(bene_id))

                    bene = User.objects.get(username=bene_id)
                    bene.received_amount += amount
                    bene.save()
                    benewallet = WalletHistory()
                    benewallet.user_id = str(bene_id)
                    benewallet.amount = float(amount)
                    benewallet.type = "credit"
                    benewallet.comment = "received from {}".format(str(user_id))
                    
                    model = MoneyTransfers()
                    model.user_id = str(user_id)
                    model.bene_id = str(bene_id)
                    model.amount = amount
                    model.txn_id = txnid
                    model.status = status
                    model.save()
                    userwallet.save()
                    benewallet.save()
                    message = "Fund Transferred"
                else:
                    message = "Internal Server Error"
        else:
            message = "Not Enough Balance"
    else:
        message = ""
    return render(request, 'wallets/transfer.html', {"message": message})

@login_required
def checkOperator(request):
    mobile = ''
    circle = ''
    data = ''
    get_response = ''
    operator = ''
    circle = ''
    sata = ''
    message = ''
    recharges = Recharges.objects.filter(user_id=request.user.username).order_by('-created_at').exclude(created_at=None)
    if request.method=="POST" and 'mobile' in request.POST:
        mobile = request.POST.get('mobile')
        operator = request.POST.get('operator')
        circle = request.POST.get('circle')
        if mobile != '' and operator != '' :
            def xyz(operator):
                time = timezone.now()
                # secret = '1451-600d130516c8f-989033'
                secret = '3554-600d147d7f55b-662250'
                email = 'balistarkumar091297@gmail.com'
                url = "https://services.apiscript.in/jwt_encode"
                # username = "APIHA10337901"
                username = "APIHA3178876"
                # password = "Smarty@248"
                password = 113239

                payload = "secret_key={}&email_id={}".format(secret, email)
                headers = {
                    'content-type': "application/x-www-form-urlencoded",
                    'cache-control': "no-cache",
                    'postman-token': "397273e7-d3b6-416d-c7ce-ffeb722adaf9"
                    }

                response = requests.request("POST", url, data=payload, headers=headers)
                data = response.json()
                encode_token = data['encode_token']

                url = "http://staging.apiscript.in/recharge/plan"

                payload = "username={}&pwd={}&operator={}&token={}".format(username, password, operator, encode_token)
                headers = {
                    'content-type': "application/x-www-form-urlencoded",
                    'authorization': "Digest username=\"\", realm=\"\", nonce=\"\", uri=\"/dmt/express_fund_transfer\", response=\"3e73127784fc3e52ccf0b55e91c87c4b\", opaque=\"\"",
                    'cache-control': "no-cache",
                    'postman-token': "2d2d3007-a70b-2dda-e781-c47221c45df9"
                    }

                response = requests.request("POST", url, data=payload, headers=headers)

                return response.json()
            sata = xyz(operator)['plan']
            data = []
            if circle == 'All Circles':
                for x in sata:
                    data.append(x)
            else:
                for x in sata:
                    if x['circle'] == circle:
                        data.append(x)

    return render(request, 'users/recharge.html', {
        'message': message,
        'getplans': data,
        'mobile': mobile,
        'operator': operator,
        'recharges': recharges,
    })

from django.utils.crypto import get_random_string

@login_required
def recharge(request):
    message = ""
    error = 0

    def xyz(ty_pe, mobile, amount, operator, txnid):
                time = timezone.now()
                secret = '1451-600d130516c8f-989033'
                email = 'balistarkumar091297@gmail.com'
                url = "https://services.apiscript.in/jwt_encode"
                username = "APIHA10337901"
                password = "Smarty@248"

                payload = "secret_key={}&email_id={}".format(secret, email)
                headers = {
                    'content-type': "application/x-www-form-urlencoded",
                    'cache-control': "no-cache",
                    'postman-token': "397273e7-d3b6-416d-c7ce-ffeb722adaf9"
                    }

                response = requests.request("POST", url, data=payload, headers=headers)
                data = response.json()
                encode_token = data['encode_token']

                # Recharge
                url = "https://services.apiscript.in/recharge/api"

                payload = "username={}&pwd={}&operatorcode={}&number={}&amount={}&client_id={}&token={}".format(username, password, operator, mobile, amount, txnid, encode_token)
                headers = {
                    'content-type': "application/x-www-form-urlencoded",
                    'authorization': "Digest username=\"\", realm=\"\", nonce=\"\", uri=\"/dmt/express_fund_transfer\", response=\"3e73127784fc3e52ccf0b55e91c87c4b\", opaque=\"\"",
                    'cache-control': "no-cache",
                    'postman-token': "2d2d3007-a70b-2dda-e781-c47221c45df9"
                    }

                response = requests.request("POST", url, data=payload, headers=headers)

                return response.json()

    def generateid():
        txnid = randint(1111111, 99999999)
        try:
            txn = Recharges.objects.get(transaction_id = txnid)
        except Recharges.DoesNotExist:
            txn = 0
        if txn:
            generateid()
        else:
            return txnid

    def userbal(user):
        userid = User.objects.get(username=user)
        bal = userid.income + userid.binary_income + userid.added_amount + userid.received_amount 
        # + userid.new_funds
        return bal


    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        operator = request.POST.get('operator')
        amount = float(request.POST.get('amount'))
        ty_pe = request.POST.get('type')
        txnid = generateid()
        user = 'JR{}'.format(txnid)
        error = 0

        if operator == 'Jio':
            operator = 'MJ'
        elif operator == 'Airtel':
            operator = 'MA'
        elif operator == 'Vodafone' or operator == 'Idea':
            operator = 'MV'
        else:
            operator = 'Not Found'

        print(request.user)
        userbal = userbal(str(request.user))
        amount = float(request.POST.get('amount'))
        try:
            binary = BinaryTree.objects.get(user=request.user).active
        except Exception as e:
            binary = False
        if request.user.new_funds + 250 - request.user.recharge_limit_used >= amount and binary:
            if request.user.recharge_limit < 250:
                amount = 10000
            nf_debit = amount - (250 - request.user.recharge_limit_used)
            if nf_debit < 0:
                nf_debit = 0
            if request.user.recharge_limit_used + amount <= 250:
                amount = float(request.POST.get('amount'))  
                recharge = xyz(ty_pe, mobile, amount, operator, txnid)
                status = recharge.get('message')
                try:
                    status = recharge.get('recharge_status')
                except Exception as e:
                    status = recharge.get('message')
                    error = 1
                status = str(status)
                if status.upper() == 'SUCCESS' or status.upper() == 'PENDING':  
                    rec = request.user  
                    rec.recharge_limit += 1 
                    rec.save()  
                    amount = float(request.POST.get('amount'))  
                    user_id = request.user  
                    if user_id.cash_back+user_id.secondary_cashback > amount/100:   
                        if user_id.cash_back > amount/100:  
                            user_id.cash_back = user_id.cash_back-amount/100    
                            amount = amount - amount/100    
                        else:   
                            user_id.secondary_cashback = user_id.secondary_cashback-amount/100  
                            amount = amount - amount/100

                    rcl_debit = amount - nf_debit
                    if rcl_debit > 0:
                        userr = request.user
                        userr.recharge_limit_used += rcl_debit
                        userr.recharge_limit -= rcl_debit
                        amount -= rcl_debit
                        userr.save()

                    if nf_debit > 0:
                        user_id.new_funds = user_id.new_funds - nf_debit  
                        print(amount)   
                        amount = 0

                    user_id.save()  
                    amount = float(request.POST.get('amount'))  
                    userwallet = WalletHistory()  
                    userwallet.user_id = str(user_id)   
                    userwallet.amount = float(amount - amount/100)  
                    userwallet.type = "debit"   
                    userwallet.comment = "spent on recharge"    

                    amount = float(request.POST.get('amount'))  
                    userspend = WalletHistory()   
                    userspend.user_id = str(user_id)    
                    userspend.amount = amount/100   
                    userspend.type = "debit"    
                    userspend.comment = "Reward Points debit"   

                    amount = float(request.POST.get('amount'))  
                    model = Recharges() 
                    model.user_id = str(user_id)    
                    model.amount = amount   
                    model.mobile_number = mobile    
                    model.transaction_id = txnid    
                    model.order_id = txnid 
                    model.operator = operator   
                    model.status = status   
                    model.save()    

                    userid = request.user   

                    def finduplines(user):  
                        try:    
                            user = User.objects.get(username__iexact=str(user)) 
                            upline = user.referal   
                        except User.DoesNotExist:   
                            upline = 'blank'    
                        return upline   

                    levels = {  
                    'level1': 0.3/100,  
                    'level2': 0.25/100, 
                    'level3': 0.20/100, 
                    'level4': 0.15/100, 
                    'level5': 0.10/100, 
                    'level6': 0.10/100, 
                    'level7': 0.10/100, 
                    'level8': 0.10/100, 
                    'level9': 0.10/100, 
                    'level10': 0.10/100,    
                    }   

                    level = 0   
                    upline_user = userid.referal    
                    userid = request.user   
                    amount = float(request.POST.get('amount'))  
                    uplines = [upline_user, ]
                    while level < 9 and upline_user != 'blank':
                        upline_user = finduplines(str(upline_user))
                        uplines.append(upline_user)
                        level += 1

                    level = 1
                    for upline in uplines:
                        try:
                            upline_user = User.objects.get(username=upline) 
                        except Exception as e:  
                            upline_user = 'blank'   
                        if upline_user != 'blank':  
                            upline_amount = levels['level{}'.format(level)]*amount*0.70 
                            upline_user.income += upline_amount*0.9 
                            upline_user.total_income  += upline_amount  
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = upline  
                            upline_wallet.amount = upline_amount    
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "new recharge done by your level{} user".format(level)  
                            upline_user.save()  
                            upline_wallet.save()    
                        level = level + 1   
                    userid.income += 0.02*amount*0.9*0.70   
                    userid.total_income  += 0.02*amount*0.70    
                    usewallet = WalletHistory()   
                    usewallet.user_id = str(userid) 
                    usewallet.amount = 0.02*amount*0.70 
                    usewallet.type = "credit"   
                    usewallet.comment = "Recharge cashback" 
                    userid.save()   
                    usewallet.save()    
                    userspend.save()    
                    userwallet.save()   
                    message = "Recharge Succesful on mobile {} with txn id {} and amount {}".format(mobile, txnid, amount)  
                else:   
                    message = 'Operator Down, Please try again after some time!'
            else:
                message = "Monthly Recharge Limit Crossed"
        else:
            message = "Something went wrong!"
    else:
        message = "Internal Server Error"

    if error == 1:
        message = "Operator server down, Error: " + status

    return render(request, 'users/recharge.html', {
        'message': message
    })

@login_required
def paymentoptions(request): 
    message = ""
    try:
        model = PaymentOption.objects.get(user=request.user.username)
    except Exception as e:
        model = 'blank'
    if model != 'blank':
        model.user = request.user.username
        model.save()

    if request.method == 'POST':
        name = request.POST.get('name')
        account1 = request.POST.get('account1')
        account2 = request.POST.get('account2')
        ifsc = request.POST.get('ifsc')
        bank = request.POST.get('bank')
        if account1 == account2:
            try:
                user = request.user
                try:
                    model = PaymentOption.objects.get(user=request.user.username)
                except Exception as e:
                    model = 'blank'
                if model != 'blank':
                    model.name = name
                    model.account_number = account1
                    model.ifsc = ifsc
                    model.user = user.username
                    model.status = None
                    model.bank = bank
                    model.save()
                else:
                    model = PaymentOption()
                    model.name = name
                    model.account_number = account1
                    model.ifsc = ifsc
                    model.user = user.username
                    model.status = None
                    model.bank = bank
                    model.save()
            except Exception as e:
                message = "Error 500 {}".format(e)
        else:
            message = 'Please type same account number in both fields!'

    return render(request, 'users/account.html', {'model': model, 'message': message})

@login_required
def neft(request):
    def generateid():
        txnid = randint(1000,9999)
        txnid = '220022{}'.format(txnid)
        try:
            txn = MetatraderAccount.objects.get(account=txnid, generated=True)
        except MetatraderAccount.DoesNotExist:
            txn = 0
        if txn:
            generateid()
        else:
            return txnid
    message = ""
    withdrawals = Withdrawal.objects.filter(user=request.user.username)
    try:
        mt5 = MetatraderAccount.objects.get(user=request.user.username, generated=True)
    except Exception as e:
        mt5 = 'blank' 
    mt5s = MetatraderAccount.objects.filter(user=request.user.username).exclude(generated=False).count()
    if request.method == 'POST' and 'password' in request.POST:
        password = request.POST.get('password')
        account = generateid()
        mt = MetatraderAccount()
        mt.password = password
        mt.account = account
        mt.user = request.user
        mt.save()
        user_id = request.user
        subject = 'MT5 Account Generate Request from BNXG'
        html_message = render_to_string('account/email/ipay-generate.html', {'name': user_id.name, 'username':user_id.username, 'email':user_id.email, 'mt5':account, 'amount':password, 'id': mt.id})
        plain_message = strip_tags(html_message)
        from_email = 'support@BNXG.com'
        to = 'partner@dibortfx.com'

        send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[to], html_message=html_message)
        url = "http://2factor.in/API/V1/99254625-e54d-11eb-8089-0200cd936042/ADDON_SERVICES/SEND/PSMS"
        payload = "{'From': 'TFCTOR', 'Msg': 'Hello World', 'To': '7000934949,'}"
        response = requests.request("GET", url, data=payload)
        print(response.text)
        return redirect('/wallet/mt5-transfer/')


    if request.method == 'POST' and 'mt5' in request.POST:
        if 'auto_neft' in request.POST:
            u = request.user
            if u.auto_neft == False:
                u.auto_neft = True
            else:
                u.auto_neft = False
            u.save()

        if not 'auto_neft' in request.POST:
            user_id = request.user
            amount = request.user.wallet
            try:
                payment_o = PaymentOption.objects.get(user=user_id)
                kyc = ImageUploadModel.objects.get(user=user_id)
                verify = True
            except Exception as e:
                verify = False
            try:
                if verify == True:
                    if True:
                        if request.user.wallet >= amount:
                            user_id.wallet = user_id.wallet - amount
                            model = Withdrawal()
                            model.user = user_id
                            model.amount = amount
                            model.description = ''
                            model.total_amount = amount*95/100
                            model.admin_fees = 0
                            model.tax = amount*5/100
                            model.status = 'pending'
                            model.name = payment_o.name
                            model.account_number = payment_o.mt5_account
                            model.ifsc = payment_o.ifsc

                            userwallet = WalletHistory()
                            userwallet.user_id = str(user_id)
                            userwallet.amount = float(amount) 
                            userwallet.type = "debit"
                            userwallet.filter = "MT5"
                            userwallet.comment = "MT5 Transfer"

                            userwallet.save()
                            user_id.save()
                            model.save()
                            subject = 'MT5 Transfer Request from BNXG'
                            html_message = render_to_string('account/email/ipay.html', {'name': user_id.name, 'username':user_id.username, 'email':user_id.email, 'mt5':payment_o.mt5_account, 'amount':amount*0.95, 'id': model.id})
                            plain_message = strip_tags(html_message)
                            from_email = 'support@BNXG.com'
                            to = 'partner@dibortfx.com'

                            send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[to], html_message=html_message)
                            url = "http://2factor.in/API/V1/99254625-e54d-11eb-8089-0200cd936042/ADDON_SERVICES/SEND/PSMS"
                            payload = "{'From': 'TFCTOR', 'Msg': 'Hello World', 'To': '7000934949,'}"
                            response = requests.request("GET", url, data=payload)
                            print(response.text)
                            # send_mail("", "Please transfer following amount to given MT5 account. <br> Name: {}, User id: {}, Email: {}, MT5 Account: {}, Amount: {}".format(user_id.name, user_id.username, user_id.email, payment_o.mt5_account, amount*0.95), "support@BNXG.com", ['rds0751@gmail.com',])
                            message = "MT5 Transfer Request Received!"
                        else:
                            message = "Not Enough Balance in Redeemable Wallet!"
                    else:
                        message = "Please Enter Amount in multiples of 100!"
                else:
                    message = "MT5 Services are in maintenance"
            except Exception as e:
                message = "Error 500 {}".format(e)

    if request.method == 'POST' and 'dcxa' in request.POST:
        if 'auto_neft' in request.POST:
            u = request.user
            if u.auto_neft == False:
                u.auto_neft = True
            else:
                u.auto_neft = False
            u.save()

        if not 'auto_neft' in request.POST:
            user_id = request.user
            amount = request.user.wallet
            try:
                levelp = LevelUser.objects.get(user=request.user)
            except Exception as e:
                levelp = 'None'
            total_days = levelp.level.expiration_period * 30
            rate = levelp.level.return_amount/total_days
            amount = (rate*30)

            try:
                payment_o = PaymentOption.objects.get(user=user_id)
                kyc = ImageUploadModel.objects.get(user=user_id)
                verify = True
            except Exception as e:
                verify = False
            try:
                if verify == True:
                    if True:
                        if True:
                            user_id.wallet = user_id.wallet - amount
                            model = Withdrawal()
                            model.user = user_id
                            model.amount = amount
                            model.description = ''
                            model.total_amount = amount*95/100
                            model.admin_fees = 0
                            model.tax = amount*5/100
                            model.status = 'pending'
                            model.name = payment_o.name
                            model.account_number = payment_o.mt5_account
                            model.ifsc = payment_o.ifsc

                            userwallet = WalletHistory()
                            userwallet.user_id = str(user_id)
                            userwallet.amount = float(amount) 
                            userwallet.type = "debit"
                            userwallet.filter = "DCXa"
                            userwallet.comment = "DCXa Transfer"

                            url = "http://app.dcxa.io/api/webservice.asmx/signup"

                            payload = "name={}&mobile={}&email={}&password=DCXa1234&sponsorid=DCXa-999999&withdraw_amount={}&code=IPAYMATIC3456789012".format(request.user.name, request.user.mobile, request.user.email, amount)
                            headers = {
                                'content-type': "application/x-www-form-urlencoded",
                                'cache-control': "no-cache",
                                'postman-token': "301c3688-89d1-ce66-9d44-68353aa780a5"
                                }

                            response = requests.request("POST", url, data=payload, headers=headers)

                            print(response.text)

                            userwallet.save()
                            user_id.save()
                            model.save()
                            subject = 'DCXa Transfer Request from BNXG'
                            html_message = render_to_string('account/email/ipay.html', {'name': user_id.name, 'username':user_id.username, 'email':user_id.email, 'mt5':payment_o.mt5_account, 'amount':amount*0.95, 'id': model.id})
                            plain_message = strip_tags(html_message)
                            from_email = 'support@BNXG.com'
                            to = 'support@dcxa.io'

                            send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[to], html_message=html_message)
                            url = "http://2factor.in/API/V1/99254625-e54d-11eb-8089-0200cd936042/ADDON_SERVICES/SEND/PSMS"
                            payload = "{'From': 'TFCTOR', 'Msg': 'Hello World', 'To': '7000934949,'}"
                            response = requests.request("GET", url, data=payload)
                            print(response.text)
                            # send_mail("", "Please transfer following amount to given MT5 account. <br> Name: {}, User id: {}, Email: {}, MT5 Account: {}, Amount: {}".format(user_id.name, user_id.username, user_id.email, payment_o.mt5_account, amount*0.95), "support@BNXG.com", ['rds0751@gmail.com',])
                            message = "DCXa Transfer Request Received!"
                        else:
                            message = "Not Enough Balance in Redeemable Wallet!"
                    else:
                        message = "Please Enter Amount in multiples of 100!"
                else:
                    message = "MT5 Services are in maintenance"
            except Exception as e:
                message = "Error 500 {}".format(e)

    return render(request, 'users/mt5.html', {'message': message, 'withdrawals': withdrawals, 'mt5': mt5, 'mt5s': mt5s})

@login_required
def history(request):
    user = request.user
    page = request.GET.get('page', 1)
    history_list = WalletHistory.objects.filter(user_id=str(user)).order_by('-created_at')
    paginator = Paginator(history_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        histories = paginator.page(page)
    except(EmptyPage, InvalidPage):
        histories = paginator.page(1)

    wstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-600)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    mwhs = WalletHistory.objects.filter(created_at__range=(mstart_date, mend_date), user_id=str(user))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date), user_id=str(user))
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date), user_id=str(user))
    dincome = 0
    wincome = 0
    mincome = 0
    try:
        fake = FakeHistory.objects.get(user=user)
    except Exception as e:
        fake = 'blank'
    if fake == 'blank':
        for wh in wwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                wincome += wh.amount
        for wh in dwhs:
            if wh.type != None:
                if 'credit' in wh.type or 'income' in wh.type:
                    dincome += wh.amount
        for wh in mwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                mincome += wh.amount
    else:
        dincome = fake.total
        mincome = fake.month
        wincome = fake.week

    # Get the index of the current page
    index = histories.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    print(dincome,mincome,wincome)
    return render(request, 'users/incomehistory.html', {'histories':histories, 'page_range': page_range, 'd': dincome, 'm': mincome, 'w': wincome})

@login_required
def pool(request):
    user = request.user
    page = request.GET.get('page', 1)
    history_list = WalletHistory.objects.filter(user_id=str(user), comment__icontains='Global autopool non wo').order_by('-created_at')
    paginator = Paginator(history_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        histories = paginator.page(page)
    except(EmptyPage, InvalidPage):
        histories = paginator.page(1)

    wstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-600)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    mwhs = WalletHistory.objects.filter(created_at__range=(mstart_date, mend_date), user_id=str(user))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date), user_id=str(user))
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date), user_id=str(user))
    dincome = 0
    wincome = 0
    mincome = 0
    try:
        fake = FakeHistory.objects.get(user=user)
    except Exception as e:
        fake = 'blank'
    if fake == 'blank':
        for wh in wwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                wincome += wh.amount
        for wh in dwhs:
            if wh.type != None:
                if 'credit' in wh.type or 'income' in wh.type:
                    dincome += wh.amount
        for wh in mwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                mincome += wh.amount
    else:
        dincome = fake.total
        mincome = fake.month
        wincome = fake.week

    # Get the index of the current page
    index = histories.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    print(dincome,mincome,wincome)
    return render(request, 'wallets/pool.html', {'histories':histories, 'page_range': page_range, 'd': dincome, 'm': mincome, 'w': wincome})

@login_required
def level(request):
    user = request.user
    page = request.GET.get('page', 1)
    history_list = WalletHistory.objects.filter(user_id=str(user), comment__icontains='New Upgrade').order_by('-created_at')
    paginator = Paginator(history_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        histories = paginator.page(page)
    except(EmptyPage, InvalidPage):
        histories = paginator.page(1)

    wstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-600)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    mwhs = WalletHistory.objects.filter(created_at__range=(mstart_date, mend_date), user_id=str(user))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date), user_id=str(user))
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date), user_id=str(user))
    dincome = 0
    wincome = 0
    mincome = 0
    try:
        fake = FakeHistory.objects.get(user=user)
    except Exception as e:
        fake = 'blank'
    if fake == 'blank':
        for wh in wwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                wincome += wh.amount
        for wh in dwhs:
            if wh.type != None:
                if 'credit' in wh.type or 'income' in wh.type:
                    dincome += wh.amount
        for wh in mwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                mincome += wh.amount
    else:
        dincome = fake.total
        mincome = fake.month
        wincome = fake.week

    # Get the index of the current page
    index = histories.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    print(dincome,mincome,wincome)
    return render(request, 'wallets/level.html', {'histories':histories, 'page_range': page_range, 'd': dincome, 'm': mincome, 'w': wincome})

@login_required
def rewards(request):
    user = request.user
    page = request.GET.get('page', 1)
    history_list = WalletHistory.objects.filter(user_id=str(user), comment__icontains='Permanent').order_by('-created_at')
    paginator = Paginator(history_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        histories = paginator.page(page)
    except(EmptyPage, InvalidPage):
        histories = paginator.page(1)

    wstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-600)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    mwhs = WalletHistory.objects.filter(created_at__range=(mstart_date, mend_date), user_id=str(user))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date), user_id=str(user))
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date), user_id=str(user))
    dincome = 0
    wincome = 0
    mincome = 0
    try:
        fake = FakeHistory.objects.get(user=user)
    except Exception as e:
        fake = 'blank'
    if fake == 'blank':
        for wh in wwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                wincome += wh.amount
        for wh in dwhs:
            if wh.type != None:
                if 'credit' in wh.type or 'income' in wh.type:
                    dincome += wh.amount
        for wh in mwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                mincome += wh.amount
    else:
        dincome = fake.total
        mincome = fake.month
        wincome = fake.week

    # Get the index of the current page
    index = histories.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    print(dincome,mincome,wincome)
    return render(request, 'wallets/rewards.html', {'histories':histories, 'page_range': page_range, 'd': dincome, 'm': mincome, 'w': wincome})

@login_required
def referral(request):
    user = request.user
    page = request.GET.get('page', 1)
    history_list = WalletHistory.objects.filter(user_id=str(user), comment__icontains='More than').order_by('-created_at')
    paginator = Paginator(history_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        histories = paginator.page(page)
    except(EmptyPage, InvalidPage):
        histories = paginator.page(1)

    wstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-600)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    mwhs = WalletHistory.objects.filter(created_at__range=(mstart_date, mend_date), user_id=str(user))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date), user_id=str(user))
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date), user_id=str(user))
    dincome = 0
    wincome = 0
    mincome = 0
    try:
        fake = FakeHistory.objects.get(user=user)
    except Exception as e:
        fake = 'blank'
    if fake == 'blank':
        for wh in wwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                wincome += wh.amount
        for wh in dwhs:
            if wh.type != None:
                if 'credit' in wh.type or 'income' in wh.type:
                    dincome += wh.amount
        for wh in mwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                mincome += wh.amount
    else:
        dincome = fake.total
        mincome = fake.month
        wincome = fake.week

    # Get the index of the current page
    index = histories.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    print(dincome,mincome,wincome)
    return render(request, 'wallets/referral.html', {'histories':histories, 'page_range': page_range, 'd': dincome, 'm': mincome, 'w': wincome})

@login_required
def royalty(request):
    user = request.user
    page = request.GET.get('page', 1)
    history_list = WalletHistory.objects.filter(user_id=str(user), comment__icontains='royalty').order_by('-created_at')
    paginator = Paginator(history_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        histories = paginator.page(page)
    except(EmptyPage, InvalidPage):
        histories = paginator.page(1)

    wstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-600)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    mwhs = WalletHistory.objects.filter(created_at__range=(mstart_date, mend_date), user_id=str(user))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date), user_id=str(user))
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date), user_id=str(user))
    dincome = 0
    wincome = 0
    mincome = 0
    try:
        fake = FakeHistory.objects.get(user=user)
    except Exception as e:
        fake = 'blank'
    if fake == 'blank':
        for wh in wwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                wincome += wh.amount
        for wh in dwhs:
            if wh.type != None:
                if 'credit' in wh.type or 'income' in wh.type:
                    dincome += wh.amount
        for wh in mwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                mincome += wh.amount
    else:
        dincome = fake.total
        mincome = fake.month
        wincome = fake.week

    # Get the index of the current page
    index = histories.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    print(dincome,mincome,wincome)
    return render(request, 'wallets/royalty.html', {'histories':histories, 'page_range': page_range, 'd': dincome, 'm': mincome, 'w': wincome})

@login_required
def rank(request):
    user = request.user
    page = request.GET.get('page', 1)
    history_list = WalletHistory.objects.filter(user_id=str(user), comment__icontains='rank').order_by('-created_at')
    paginator = Paginator(history_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        histories = paginator.page(page)
    except(EmptyPage, InvalidPage):
        histories = paginator.page(1)

    wstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-600)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    mwhs = WalletHistory.objects.filter(created_at__range=(mstart_date, mend_date), user_id=str(user))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date), user_id=str(user))
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date), user_id=str(user))
    dincome = 0
    wincome = 0
    mincome = 0
    try:
        fake = FakeHistory.objects.get(user=user)
    except Exception as e:
        fake = 'blank'
    if fake == 'blank':
        for wh in wwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                wincome += wh.amount
        for wh in dwhs:
            if wh.type != None:
                if 'credit' in wh.type or 'income' in wh.type:
                    dincome += wh.amount
        for wh in mwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                mincome += wh.amount
    else:
        dincome = fake.total
        mincome = fake.month
        wincome = fake.week

    # Get the index of the current page
    index = histories.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    print(dincome,mincome,wincome)
    return render(request, 'wallets/rank.html', {'histories':histories, 'page_range': page_range, 'd': dincome, 'm': mincome, 'w': wincome})

@login_required
def imps(request):
    
    return render(request, 'users/transferamount.html')

@login_required
def mt5t(request):
    try:
        mt = Mtw.objects.get(user_id=request.user)
    except Exception as e:
        mt = 0
    wt = WalletHistory.objects.filter(user_id=request.user.username, comment="Sent to DCXa")
    if wt.count() == 0:
        show = True
    else:
        show = False
    print(show)
    if request.method == "POST" and 'mt5' in request.POST:
        user = request.user
        url = "https://admin.dibortfx.com/modules/ThirdParty/api.php"

        values = '{{"firstname":"{0}","lastname":" ","email":"{1}","birthday":"02-12-1995","country_name":"India","mobile":"{2}","mailingstreet":"{3}","mailingcity":"usercity","mailingpobox":"110011","reference_id":"110011","live_metatrader_type":"MT5","live_label_account_type":"B_IPAY_IPAY","live_currency_code":"USD","leverage":"300"}}'
        payload={
        '_operation': 'dibortCreateContact',
        'values': values.format(user.name, user.email, user.mobile, user.address)
        }
        
        headers = {
        'Authorization': 'Basic YWRtaW46SmZuS3RwZTlDTk03dTVyTFFVN0FqbnpGeng1Sk9CYWF2MU5uQGFhRGZDIUBkZ2g='
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        res = response.json()
        account = res.get('result').get('live_details').get('account_no')
        user.otp = account
        user.rank = res.get('result').get('live_details').get('contactid')[-5:]
        user.save()
        url = "https://admin.dibortfx.com/modules/ThirdParty/api.php"
        amount = request.user.wallet

        payload={
        '_operation': 'dibortCreateDeposit',
        'values': '{{"contactid":"12x{0}","payment_from":"IPAY","payment_currency":"USD","payment_to":"{1}","amount":"{2}"}}'.format(request.user.rank, request.user.otp, request.user.wallet)
        }
        user = request.user
        user.withdrawal += amount
        user.wallet = 0
        user.save()
        wallet = WalletHistory()
        wallet.user_id = user.username
        wallet.amount = amount
        wallet.comment = "Sent to MT5"
        wallet.type = 'debit'
        wallet.save()
        user.save()
        response = requests.request("POST", url, headers=headers, data=payload)
        title = 'Thankyou!'
        message = 'Your amount sent is being processed, please wait for 24-48 hrs'
        return render(request,"level/thankyou.html", {'title': title, 'message': message})
    if request.method == "POST" and 'dcxa' in request.POST:
        user = request.user
        try:
            levelp = LevelUser.objects.get(user=request.user)
        except Exception as e:
            levelp = 'None'
        total_days = levelp.level.expiration_period * 30
        rate = levelp.level.return_amount/total_days
        amount = (rate*30)
        url = "http://app.dcxa.io/api/webservice.asmx/signup"

        payload = "name={}&mobile=&email={}&password=DCXa1234&sponsorid=DCXa-999999&withdraw_amount={}&code=IPAYMATIC3456789012".format(request.user.name, request.user.email, amount)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'postman-token': "301c3688-89d1-ce66-9d44-68353aa780a5"
            }
        print(payload)

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        res = response.json()
        account = res.get('userid')
        status = res.get('status')
        if status == '1':    
            user.dcxa_id = account
            user.save()
            url = "https://admin.dibortfx.com/modules/ThirdParty/api.php"

            payload={
            '_operation': 'dibortCreateDeposit',
            'values': '{{"contactid":"12x{0}","payment_from":"IPAY","payment_currency":"USD","payment_to":"{1}","amount":"{2}"}}'.format(request.user.rank, request.user.otp, request.user.wallet)
            }
            user = request.user
            user.withdrawal += amount
            user.wallet = 0
            user.save()
            wallet = WalletHistory()
            wallet.user_id = user.username
            wallet.amount = amount
            wallet.comment = "Sent to DCXa"
            wallet.type = 'debit'
            wallet.save()
            user.save()
            response = requests.request("POST", url, headers=headers, data=payload)
            title = 'Thankyou!'
            message = 'Your amount sent to DCXa & is being processed, please wait for 24-48 hrs'
            return render(request,"level/thankyou.html", {'title': title, 'message': message})
        else:
            title = 'Invalid Request!'
            message = 'Something went wrong please contact admin'
            return render(request,"level/thankyou.html", {'title': title, 'message': message})
    return render(request,"users/mt5.html", {"mt": mt, 'show': show})


@login_required
def send(request):
    message = "Please open right page"
    def userbal(user):
        userid = User.objects.get(username=user)
        bal = userid.income + userid.binary_income + userid.new_funds
        return bal

    def generateid():
        txnid = get_random_string(8)
        try:
            txn = WalletHistory.objects.get(txnid = txnid)
        except WalletHistory.DoesNotExist:
            txn = 0
        if txn:
            generateid()
        else:
            return 'JR{}'.format(txnid)

    def sendmoney(mobile, amount, bid, txnid):
        url = "https://www.mobilerechargenow.com/api/v2/dmt/transfer.php?username=MRN1747997&apikey=1348504980&number={}&amount={}&beneficiaryid={}&txnid={}&format=json".format(mobile, amount, bid, txnid)
        r = requests.get(url)
        data = r.json()
        status = data[
        'status'
        ]
        return status, data

    if request.method == 'POST':
        bid = request.POST.get('bid')
        bac = Beneficiary.objects.get(bene_id=bid)
        amount = float(request.POST.get('amount'))
        mobile = request.user.mobile
        # bac.mobile_number
        txnid = generateid()

    userbal = userbal(str(request.user))
    user_id = request.user

    # if request.user.redeem_access == True:
    #     if amount < 5001 and amount >= 200:
    #         if user_id.imps_daily+amount > 5001:
    #             if userbal >= amount:
    #                 if user_id.income <= amount:
    #                     amount = amount - user_id.income
    #                     user_id.income = 0
    #                     print("if1")
    #                     if user_id.binary_income <= amount:
    #                         amount = amount - user_id.binary_income
    #                         user_id.binary_income = 0
    #                         print("if2")
    #                     else:
    #                         user_id.binary_income = user_id.binary_income - amount
    #                         amount = 0
    #                         print("if6")
    #                 else:
    #                     user_id.income = user_id.income - amount
    #                     amount = 0
    #                 print("if7")
    #                 amount = float(request.POST.get('amount'))
    #                 if amount>500:
    #                     bank = '2%'
    #                     sendmoney, sdata = sendmoney(mobile, amount*0.98, bid, txnid)
    #                 else:
    #                     bank = '3%'
    #                     sendmoney, sdata = sendmoney(mobile, amount*0.97, bid, txnid)

    #                 if sendmoney != 'FAILED':
    #                     userwallet = WalletHistory()
    #                     userwallet.balance_after = userbal - amount
    #                     userwallet.user_id = str(user_id)
    #                     userwallet.amount = float(amount)
    #                     userwallet.type = "debit"
    #                     userwallet.filter = "IMPS"
    #                     userwallet.txnid = txnid
    #                     userwallet.comment = "Sent to bank with txnid {}".format(txnid)
    #                     user_id.imps_daily += amount

    #                     userwallet.save()
    #                     user_id.save()
    #                     message = "Money sent successfully sent with amount {} and bank charges {}".format(amount, bank)
    #                 else:
    #                     message = "third party server down, support email sent to third party"
    #             else:
    #                 message = "not enough available balance in wallet"
    #         else:
    #             message = "daily limit exceeded, 5000 is the limit"
    #     else:
    #         message = "You can transfer more than 200 and less than 5000 only"
    if request.user.new_funds >= amount and request.user.redeem_access == False:
        directs = Shopping.objects.filter(direct=request.user).count()
        if directs >= 2 or request.user.new_funds >= amount:
            if amount <= 2001 and amount >= 200:
                if user_id.imps_daily+amount < 2001:
                    user_id.new_funds = user_id.new_funds - amount
                    amount = float(request.POST.get('amount'))
                    if amount>500:
                        bank = '2%'
                        sendmoney, sdata = sendmoney(mobile, amount*0.98, bid, txnid)
                    else:
                        bank = '3%'
                        sendmoney, sdata = sendmoney(mobile, amount*0.97, bid, txnid)

                    if sendmoney != 'FAILED':
                        userwallet = WalletHistory()
                        userwallet.balance_after = userbal - amount
                        userwallet.user_id = str(user_id)
                        userwallet.amount = float(amount)
                        userwallet.type = "debit"
                        userwallet.filter = "IMPS"
                        userwallet.txnid = txnid
                        userwallet.comment = "Sent to bank with txnid {}".format(txnid)
                        user_id.imps_daily += amount

                        userwallet.save()
                        user_id.save()
                        message = "Money sent successfully!".format(amount, bank)
                    else:
                        message = "Bank server down Error {}".format(sdata.get('resText'))
                else:
                    message = "daily limit exceeded, 2000 is the limits"
            else:
                message = "You can withdraw more than 200 and less than 1000 only!"
        else:
            message = "Please add 2 Shopping Directs to Withdraw Money"
    else:
        message = "Not Enough Available Balance"
    return render(request, 'users/moneytransfered.html', { 'message': message, })

def fundrequest(request):
    message = ''
    fr = FundRequest.objects.filter(user=request.user.username)

    def generateid():
        txnid = get_random_string(8)
        txnid = 'IPAY'+txnid
        try:
            txn = FundRequest.objects.get(code = txnid)
        except FundRequest.DoesNotExist:
            txn = 0
        if txn:
            generateid()
        else:
            return format(txnid)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        user = request.user
        code = generateid()
        message = 'Fund request sent'
        model = FundRequest()
        model.user = user.username
        model.amount = amount
        model.code = code
        model.save()

    return render(request, 'users/fundrequest.html', {'message': message, 'fr': fr})

from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.http import HttpResponse

@csrf_protect
@csrf_exempt
def callback(request):
    message = 'False'
    if request.method == 'POST':
        data = request.POST.get('data')
        data = eval(data)
        client_id = data.get('client_id')
        final_status = data.get('recharge_status')
    try:
        r = Recharges.objects.get(order_id=client_id)
    except Exception as e:
        r = False
    if r:
        status = r.status
        user = User.objects.get(username=r.user_id)
        if r.status.upper() == 'PENDING':
            r.status = final_status
            r.save()
    return HttpResponse(json.dumps(client_id), content_type="application/json")


def confirm_generate(request, id):
    try:
        w = MetatraderAccount.objects.get(id=id)
        if w.generated == None:
            w.generated = True
            w.save()
            message = 'Successfully submitted data'
        else:
            message = 'Please contact admin ASAP, its an unavoidable error!'
    except Exception as e:
        message = 'Please contact admin ASAP, its an unavoidable error!'
    return render(request, 'wallets/confirm.html', {'message': message})


def cancel_generate(request, id):
    try:
        w = MetatraderAccount.objects.get(id=id)
        if w.generated == None:
            w.generated = False
            w.save()
            message = 'Successfully submitted data'
        else:
            message = 'Please contact admin ASAP, its an unavoidable error!'
    except Exception as e:
        message = 'Please contact admin ASAP, its an unavoidable error!'
    return render(request, 'wallets/cancel.html', {'message': message})

def confirm_neft(request, id):
    try:
        w = Withdrawal.objects.get(id=id)
        if w.status == 'pending':
            w.status = 'Success'
            w.save()
            message = 'Successfully submitted data'
        else:
            message = 'Please contact admin ASAP, its an unavoidable error!'
    except Exception as e:
        message = 'Please contact admin ASAP, its an unavoidable error!'
    return render(request, 'wallets/confirm.html', {'message': message})


def cancel_neft(request, id):
    try:
        w = Withdrawal.objects.get(id=id)
        if w.status == 'pending':
            w.status = 'Failed'
            w.save()
            message = 'Successfully submitted data'
        else:
            message = 'Please contact admin ASAP, its an unavoidable error!'
    except Exception as e:
        message = 'Please contact admin ASAP, its an unavoidable error!'
    return render(request, 'wallets/cancel.html', {'message': message})

from django.core.mail import send_mail
from django.conf import settings

def withdrawBNXG(request):
    message = ''
    if request.method == "POST":
        otp = random.randint(100000,999999)
        request.session['email_otp'] = otp
        message = f'your otp is {otp}'
        user_email = request.user.email
        amount = float(request.POST.get('amount'))
        if amount >= 10 and amount <= request.user.wallet + request.user.pool_wallet:
            request.session['amount'] = amount
            send_mail(
                'Email Verification OTP',
                message,
                settings.EMAIL_HOST_USER,
                [user_email],
                fail_silently=False,
            )
            return redirect('/wallet/otp/')
        else:
            message = 'Low balance or enter amount greater than 10'
    
    user = request.user
    page = request.GET.get('page', 1)
    history_list = WalletHistory.objects.filter(user_id=str(user), comment__icontains='Sent to your BNXG wallet address').order_by('-created_at')
    paginator = Paginator(history_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        histories = paginator.page(page)
    except(EmptyPage, InvalidPage):
        histories = paginator.page(1)

    wstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-600)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    mwhs = WalletHistory.objects.filter(created_at__range=(mstart_date, mend_date), user_id=str(user))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date), user_id=str(user))
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date), user_id=str(user))
    dincome = 0
    wincome = 0
    mincome = 0
    try:
        fake = FakeHistory.objects.get(user=user)
    except Exception as e:
        fake = 'blank'
    if fake == 'blank':
        for wh in wwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                wincome += wh.amount
        for wh in dwhs:
            if wh.type != None:
                if 'credit' in wh.type or 'income' in wh.type:
                    dincome += wh.amount
        for wh in mwhs:
            if 'Shopping Income from' in wh.comment or 'Shopping Self Earning' in wh.comment:
                mincome += wh.amount
    else:
        dincome = fake.total
        mincome = fake.month
        wincome = fake.week

    # Get the index of the current page
    index = histories.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    print(dincome,mincome,wincome)
    context = {'message': message, 'histories':histories, 'page_range': page_range, 'd': dincome, 'm': mincome, 'w': wincome}

    return render(request,'wallets/withdraw.html', context)

from web3 import Web3
from eth_account import Account
from web3.middleware import geth_poa_middleware

def bnxg_verification(request):
    def generateid():
        txnid = get_random_string(8)
        try:
            txn = WalletHistory.objects.get(txnid = txnid)
        except WalletHistory.DoesNotExist:
            txn = 0
        if txn:
            generateid()
        else:
            return '{}'.format(txnid)
        
    message = 'Please Enter OTP'
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session['email_otp']
        if int(u_otp) == otp:
            try:
                m = Mtw.objects.get(id=8)
                pk = m.private_key
                po = PaymentOption.objects.get(user=request.user.username)

                bsc_rpc_url = 'https://bsc-dataseed.binance.org/'
                
                w3 = Web3(Web3.HTTPProvider(bsc_rpc_url))
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                abi = '[{"inputs":[{"internalType":"string","name":"name_","type":"string"},{"internalType":"string","name":"symbol_","type":"string"},{"internalType":"uint256","name":"supply_","type":"uint256"},{"internalType":"uint8","name":"decimals_","type":"uint8"},{"internalType":"bool","name":"canMint_","type":"bool"},{"internalType":"bool","name":"canBurn_","type":"bool"},{"internalType":"address","name":"addr_","type":"address"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"canBurn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"canMint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
                abi = json.loads(abi)
                token = w3.eth.contract(address='0x5DFb9C077FbDF7579ACCdd6184Ee896a16aA3942', abi=abi)

                # Wallet information
                private_key = pk
                wallet_address = po.bank

                # Contract and token information
                contract_address = '0x5DFb9C077FbDF7579ACCdd6184Ee896a16aA3942'
                token_decimals = 18  # Adjust if your token has a different number of decimals

                # Connect to BSC network

                # Create an account object from the private key
                account = Account.from_key(private_key)

                # Get the latest nonce for the account
                nonce = w3.eth.get_transaction_count(account.address)

                # Prepare the transaction data
                token_amount = int(request.session['amount']) * 10 # Amount of BUSD to send
                token_amount_in_wei = int(token_amount * 10 ** 16) * 10
                
                transaction = token.functions.transfer(po.bank, token_amount_in_wei).build_transaction({
                                    'gas':200000,
                                    'nonce': nonce,
                                    'gas': 200000,  # Adjust the gas limit if needed
                                    'gasPrice': w3.eth.gas_price
                                    })

                # Sign the transaction
                signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

                # Send the signed transaction
                txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

                # Wait for the transaction to be mined
                txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

                # Check if the transaction was successful
                if txn_receipt['status']:
                    wallet = request.user
                    wallet.wallet -= int(request.session['amount'])
                    wallet.save()
                    message = 'Transaction Success!'
                    userwallet = WalletHistory()
                    userwallet.user_id = request.user.username
                    userwallet.amount = int(request.session['amount'])
                    userwallet.type = "debit"
                    userwallet.filter = "BNXG"
                    userwallet.txnid = generateid()
                    userwallet.comment = "Sent to your BNXG wallet address"
                    userwallet.save()
                    redirect('/users/')
                else:
                    message = 'Transaction failed. Error message: ' + str(txn_receipt)
            except Exception as e:
                raise e
        else:
            message = 'Wrong OTP'

    context = {
        'message': message
    }
    return render(request,'wallets/withdrawal.html', context)
