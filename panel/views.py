from django.shortcuts import render
from django.db.models import Q, F, Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import requests
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpRequest, Http404
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required 
import datetime
from django.conf import settings
from django.contrib.auth import load_backend, login

from wallets.models import WalletHistory, Withdrawal, PaymentOption
from users.models import User
import random
from level.models import Activation, LevelIncomeSettings, LevelUser, PoolUser
import csv

@staff_member_required
def home(request):
    wstart_date = datetime.datetime.now() + datetime.timedelta(-7)
    wend_date = datetime.datetime.now()
    dstart_date = datetime.datetime.now() + datetime.timedelta(-1)
    dend_date = datetime.datetime.now()
    mstart_date = datetime.datetime.now() + datetime.timedelta(-30)
    mend_date = datetime.datetime.now()
    dwhs = WalletHistory.objects.filter(created_at__range=(dstart_date, dend_date))
    wwhs = WalletHistory.objects.filter(created_at__range=(wstart_date, wend_date))
    twhsi = WalletHistory.objects.filter(comment__icontains='Prime Upgradation')
    twhso = WalletHistory.objects.filter(comment__icontains='MT5 Transfer')
    tci = 0
    tco = 0
    for x in twhsi:
        tci += x.amount
    for x in twhso:
        tco += x.amount 
    ci = 0
    co = 0
    tre = 0
    for wh in wwhs:
        if 'Prime Upgradation' in wh.comment:
            ci += wh.amount
        elif 'MT5 Transfer' in wh.comment:
            co += wh.amount
    for wh in dwhs:
        if 'Prime Upgradation' in wh.comment:
            tre += wh.amount
    return render(request, 'panel/home.html', {'ci': ci, 'co': co, 'tre':tre, 'tci': tci, 'tco': tco})

@staff_member_required
def users(request):
    q = 'blank'
    u = User.objects.all().order_by('?')
    if request.method == 'POST':
        q = request.POST.get('q')
        u = User.objects.all().order_by('?')
        if 'q' in request.POST and len(request.POST.get('q'))>=3:
            u = User.objects.filter(username__icontains=request.POST.get('q')) or User.objects.filter(name__icontains=request.POST.get('q')) or User.objects.filter(email__icontains=request.POST.get('q')) or User.objects.filter(mobile__icontains=request.POST.get('q'))
            u = u
    for x in u:
        try:
            x.referral = User.objects.get(username=x.referral)
        except Exception as e:
            print(e)
            x.referral = x.referral
        try:
            x.top = LevelUser.objects.get(user=x.username)
        except Exception as e:
            print(e)
            x.top = 0
    return render(request, 'panel/users.html', {'u': u, 'q': q})

@staff_member_required
def user(request, id):
    print(request.POST)
    if request.method == "POST" and 'name' in request.POST:
        id_ = request.POST.get('id')
        user = User.objects.get(id=id_)
        user.name = request.POST.get('name')
        user.mobile = request.POST.get('mobile')
        user.email = request.POST.get('email')
        user.address = request.POST.get('address')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        user.referral = request.POST.get('referral')
        user.c = request.POST.get('wallet')
        user.save()
        print(request.POST)
        if request.POST.get('password') != '':
            user.password = make_password(request.POST.get('password'))
            user.save()
    if request.method == "POST" and 'account1' in request.POST:
        id_ = request.POST.get('ida')
        if id_ == '':
            p = PaymentOption()
        else:
            try:
                p = PaymentOption.objects.get(id=id_)
            except Exception as e:
                print(e)
                p = PaymentOption()
        account1 = request.POST.get('account1')
        account2 = request.POST.get('account2')
        if account1 == account2:
            p.user = request.POST.get('userid')
            p.account_number = account1
            p.name = request.POST.get('namea')
            p.ifsc = request.POST.get('ifsc')
            p.bank = request.POST.get('bank')
            p.mt5_account = request.POST.get('mt5_account')
            verified = request.POST.get('verified')
            if verified == 'on':
                p.status = True
            else:
                p.status = False
            p.save()
        else:
            message = 'Please confirm account number'
    if request.method == "POST" and 'idk' in request.POST:
        id_ = request.POST.get('idk')
        if id_ == '':
            k = ImageUploadModel()
        else:
            try:
                k = ImageUploadModel.objects.get(id=id_)
            except Exception as e:
                print(e)
                k = ImageUploadModel()
        file1 = request.FILES.get('front')
        file2 = request.FILES.get('back')
        verified = request.POST.get('verified')
        k.user = request.POST.get('userid')
        if request.FILES:
            k.imageAF = file1
            k.imageAB = file2
        if verified == 'on':
            k.approved = True
        else:
            k.approved = False
        k.save()
    if request.method == "POST" and 'block' in request.POST:
        user = User.objects.get(id=id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('/m2/admin/users/')
    
    u = User.objects.get(id=id)
    try:
        k = ImageUploadModel.objects.get(user=u.username)
    except Exception as e:
        print(e)
        k = 'blank'
    try:
        b = PaymentOption.objects.get(user=u.username)
    except Exception as e:
        print(e)
        b = 'blank'
    w = Withdrawal.objects.filter(user=u.username)
    return render(request, 'panel/user.html', {'u': u, 'k': k, 'b': b, 'w': w})

@staff_member_required
def withdrawals(request):
    w = Withdrawal.objects.all()
    return render(request, 'panel/withdrawals.html', {'w': w})

@staff_member_required
def kycs(request):
    w = ImageUploadModel.objects.all()
    if request.method == 'POST':
        if 'approve' in request.POST:
            x = ImageUploadModel.objects.get(user=request.POST.get('user'))
            x.approved = True
            x.save()
        if 'reject' in request.POST:
            x = ImageUploadModel.objects.get(user=request.POST.get('user'))
            x.approved = False
            x.save()
        if 'delete' in request.POST:
            x = ImageUploadModel.objects.get(user=request.POST.get('user'))
            x.delete()
    return render(request, 'panel/kycs.html', {'w': w})

@staff_member_required
def bankdetails(request):
    w = PaymentOption.objects.all()
    if request.method == 'POST':
        if 'approve' in request.POST:
            x = PaymentOption.objects.get(user=request.POST.get('user'))
            x.status = True
            x.save()
        if 'reject' in request.POST:
            x = PaymentOption.objects.get(user=request.POST.get('user'))
            x.status = False
            x.save()
        if 'delete' in request.POST:
            x = PaymentOption.objects.get(user=request.POST.get('user'))
            x.delete()
    return render(request, 'panel/bankdetails.html', {'w': w})

@staff_member_required
def activations(request):
    w = Activation.objects.all().order_by('-created_at')
    for x in w:
        try:
            x.user = User.objects.get(username=x.user)
        except Exception as e:
            print(e)
            pass
        try:
            x.user.referral = User.objects.get(username=x.user.referral)
        except Exception as e:
            print(e)
            pass
        try:
            x.user.referral.top = LevelUser.objects.get(user=x.user.referral)
        except Exception as e:
            print(e)
            pass
    return render(request, 'panel/activations.html', {'w': w})

@staff_member_required
def ids(request):
    w = LevelUser.objects.filter(active=True).order_by('-created_at')
    if request.method == 'POST':
        fromm = request.POST.get('from')
        date = datetime.datetime.strptime(fromm, '%Y-%m-%d')
        too = request.POST.get('to')
        date = datetime.datetime.strptime(too, '%Y-%m-%d')
        w = LevelUser.objects.filter(active=True, activated_at__range=(fromm, too)).order_by('-created_at')
    for x in w:
        try:
            x.comments = Activation.objects.get(user=x.user).comments
        except Exception as e:
            print(e)
            x.comments = 'not present'
        try:
            x.user = User.objects.get(username=x.user)
        except Exception as e:
            print(e)
            pass
        try:
            x.user.referral = User.objects.get(username=x.user.referral)
        except Exception as e:
            print(e)
            pass
        x.directs = LevelUser.objects.filter(direct=x.user).count()
        try:
            x.kyc = ImageUploadModel.objects.get(user=x.user)
        except Exception as e:
            print(e)
            pass
        try:
            x.bank = PaymentOption.objects.get(user=x.user)
        except Exception as e:
            print(e)
            pass
        start_date = x.activated_at
        end_date = x.activated_at + datetime.timedelta(days=7)
        directs = LevelUser.objects.filter(direct=x.user, activated_at__range=(start_date, end_date))
        ccm = 0
        for y in directs:
            ccm += y.level.amount
        ccm_pool = 0
        if ccm >= 10000:
            ccm_pool = 12
        if ccm >= 20000:
            ccm_pool = 24
        if ccm >= 30000:
            ccm_pool = 36
        if ccm >= 40000:
            ccm_pool = 48
        if ccm >= 50000:
            ccm_pool = 60
        x.ccm_pool = ccm_pool

    return render(request, 'panel/ids.html', {'w': w})

from django.utils.crypto import get_random_string
def activate(user, amount):
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
        
    def userjoined(user):
        try:
            user = LevelUser.objects.get(user=str(user), active=True)
        except Exception as e:
            print(e)
            user = 'blank'
        print(user, '---------------')
        if user == 'blank':
            return False
        else:
            return True
        
    def autopool(user, package):
        try:
            model = PoolUser.objects.get(user=user)
        except Exception as e:
            try:
                pool_direct = PoolUser.objects.filter(downlines__lt=2).order_by('created_at')[0]
            except Exception as e:
                pool_direct = 'blank'
            model = PoolUser()
            model.user=user
            model.upline = pool_direct
            model.level = 1
            model.plan = levelp
            model.active = True
            model.save()
            if pool_direct != 'blank':
                pool_direct.downlines += 1
                pool_direct.save()
            downlines = PoolUser.objects.filter(upline=pool_direct)
            if downlines.count() >= 2:
                l1 = True
            else:
                l1 = False
            if l1 == True:
                downlines = PoolUser.objects.filter(Q(upline=downlines[1]) | Q(upline=downlines[0]))
            if downlines.count() >= 4:
                l2 = True
            else:
                l2 = False
            if l2 == True:
                downlines = PoolUser.objects.filter(Q(upline=downlines[0]) | Q(upline=downlines[1]) | Q(upline=downlines[2]) | Q(upline=downlines[3]))
            if downlines.count() >= 8:
                l3 = True
            else:
                l3 = False
            capping = pool_direct.plan.amount * 2.5
            plan = pool_direct.plan
            pool_user = User.objects.get(username=pool_direct.user)
            if True:
                pool_user = User.objects.get(username=pool_direct.user)
                level = pool_direct.level
                downlines = pool_direct.downlines
                if level == 1 and l1:
                    if plan.level == 1:
                        extra  = 4
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $4 from level 1"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                        
                    elif plan.level == 2:
                        extra  = 8
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $8 from level 1"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 3:
                        extra  = 16
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $16 from level 1"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 4:
                        extra  = 40
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $40 from level 1"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 5:
                        extra  = 80
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $80 from level 1"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 6:
                        extra  = 160
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $160 from level 1"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 7:
                        extra  = 320
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $320 from level 1"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 8:
                        extra  = 800
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $800 from level 1"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                if level == 2 and l2:
                    if plan.level == 1:
                        extra  = 8
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $8 from level 2"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 2:
                        extra  = 16
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $16 from level 2"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 3:
                        extra  = 32
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $32 from level 2"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 4:
                        extra  = 80
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $80 from level 2"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 5:
                        extra  = 160
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $160 from level 2"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 6:
                        extra  = 320
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $320 from level 2"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 7:
                        extra  = 640
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $640 from level 2"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 8:
                        extra  = 1600
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $1600 from level 2"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                if level == 3 and l3:
                    if plan.level == 1:
                        extra  = 16
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $16 from level 3"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 2:
                        extra  = 32
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $32 from level 3"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 3:
                        extra  = 64
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $64 from level 3"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 4:
                        extra  = 160
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $160 from level 3"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 5:
                        extra  = 320
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $320 from level 3"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 6:
                        extra  = 640
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $640 from level 3"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 7:
                        extra  = 1280
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $1280 from level 3"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
                    elif plan.level == 8:
                        extra  = 3200
                        if capping >= pool_user.total_income + extra:
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = pool_direct  
                            upline_wallet.amount = extra 
                            upline_wallet.balance += extra   
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "Global autopool non working income of $3200 from level 3"
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            pool_user.total_income += extra
                            pool_user.autopool_income += extra
                            pool_user.pool_wallet += extra
                            pool_user.save()
        return 0


    user = User.objects.get(username=user)
    upline_user = user.referral
    packamount = amount
    levelp = LevelIncomeSettings.objects.get(amount=packamount)
    user_id = User.objects.get(username=str(user))
    userjoined = userjoined(user)
    print(userjoined)
    if True:
        if not userjoined:
            userwallet = WalletHistory()
            userwallet.user_id = user_id
            userwallet.amount = packamount
            userwallet.type = "credit"
            userwallet.comment = "Cash for Prime Upgrade"
            userwallet.balance += packamount
            userwallet.txnid = generateid()
            userwallet.save()

            
            userwallet = WalletHistory()
            userwallet.user_id = user_id
            userwallet.amount = packamount
            userwallet.type = "debit"
            userwallet.comment = "Buying Package"
            userwallet.balance -= packamount
            userwallet.txnid = generateid()
            userwallet.save()

            userid = user   

            def finduplines(user):  
                try:    
                    user = User.objects.get(username__iexact=str(user)) 
                    upline = user.referral   
                except User.DoesNotExist:   
                    upline = 'blank'    
                return upline   

            levels = {  
                'level1': 1/100,  
                'level2': 1/100, 
                'level3': 0.75/100, 
                'level4': 0.5/100, 
                'level5': 0.25/100, 
                'level6': 0.25/100, 
                'level7': 0.25/100, 
                'level8': 0.25/100,
                'level9': 0.25/100,
                'level10': 0.25/100 
                }

            level = 0   
            upline_user = userid.referral    
            userid = user   
            amount = packamount 
            uplines = [upline_user, ]
            while level < 10 and upline_user != 'blank':
                upline_user = finduplines(str(upline_user))
                uplines.append(upline_user)
                level += 1

            level = 0
            print(uplines)
            for upline in uplines:
                try:
                    upline_user = User.objects.get(username=upline) 
                except Exception as e:
                    print(e)  
                    upline_user = 'blank'
                try:
                    upgraded = LevelUser.objects.get(user=upline, active=True)
                    capping = upgraded.level.amount * 4
                except Exception as e:
                    print(e)
                    upgraded = LevelUser.objects.get(user='BN999999')
                    capping = 0
                try:
                    upline_user = User.objects.get(username=upline) 
                except Exception as e:
                    print(e)  
                    upline_user = 'blank'
                if upline_user != 'blank' and upgraded.active:
                    upline_user.my_directs +=1 
                    upline_user.my_team += 1
                    upline_user.total_business += packamount
                    upline_user.save()
                    directs = LevelUser.objects.filter(direct=upline_user, active=True)
                    if user.referral == upline_user.username:
                        direct = True
                    else:
                        direct = False
                    upline_amount = levels['level{}'.format(level+1)]*amount

                    if direct and directs.count() == 1:
                        pairBonus = (directs[0].amount + packamount) * 0.3 * 0.95
                        if True: 
                            upline_wallet = WalletHistory()
                            upline_wallet.user_id = upline
                            upline_wallet.amount = pairBonus
                            upline_wallet.type = "credit"
                            upline_wallet.comment = "1st Pair Income"
                            upline_wallet.balance += pairBonus
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            upline_user.wallet += pairBonus
                            upline_user.today_income += pairBonus
                            upline_user.total_income += pairBonus
                            upline_user.progress += pairBonus
                            upline_user.save()
                            try:
                                upline_level_user = User.objects.get(username=upline_user.referral)
                            except Exception as e:
                                upline_level_user = 'blank'
                            if upline_level_user != 'blank':
                                upline_wallet = WalletHistory()
                                upline_wallet.user_id = upline_level_user.username
                                upline_wallet.amount = pairBonus * 0.05
                                upline_wallet.type = "credit"
                                upline_wallet.comment = "5% Upline Benefit from user {}".format(upline_user.username)
                                upline_wallet.balance += pairBonus * 0.05
                                upline_wallet.txnid = generateid()
                                upline_wallet.save()
                                upline_level_user.wallet += pairBonus * 0.05
                                upline_level_user.total_income += pairBonus * 0.05
                                upline_level_user.sponsor_income += pairBonus * 0.05
                                upline_level_user.progress += pairBonus * 0.05
                                upline_level_user.save()
                            upline_user = User.objects.get(username=upline)
                            upline_wallet = WalletHistory()
                            upline_wallet.user_id = upline
                            upline_wallet.amount = levelp.permanent_reward
                            upline_wallet.type = "credit"
                            upline_wallet.comment = "Permanent Tripod Reward"
                            upline_wallet.balance += levelp.permanent_reward
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            upline_user.wallet += levelp.permanent_reward
                            upline_user.today_income += levelp.permanent_reward
                            upline_user.total_income += levelp.permanent_reward
                            upline_user.progress += levelp.permanent_reward
                            upline_user.save()
                            upline_user = User.objects.get(username=upline)
                            autopool(upline_user.username, levelp)
                            print('if1')
                    print(directs.count(), direct, upline_user, upline_user.referral)
                    if directs.count() > 1 and direct:
                        abc = amount
                        upline_wallet = WalletHistory()
                        upline_wallet.user_id = upline
                        upline_wallet.amount = abc * 0.8
                        upline_wallet.type = "credit"
                        upline_wallet.comment = "More than 2 direct upgrades"
                        upline_wallet.balance += abc * 0.8
                        upline_wallet.txnid = generateid()
                        upline_wallet.save()
                        upline_user.wallet += abc * 0.8
                        upline_user.today_income += abc * 0.8
                        upline_user.total_income += abc * 0.8
                        upline_user.progress += abc * 0.8
                        upline_user.save()
                        upline_user = User.objects.get(username=upline)
                        print('elif1')
                    if directs.count() >= level:
                        upline_amount = levels['level{}'.format(level+1)]*amount
                        upline_wallet = WalletHistory()
                        upline_wallet.user_id = upline
                        upline_wallet.amount = upline_amount
                        upline_wallet.type = "credit"
                        upline_wallet.comment = "New Upgrade by {} in level {}".format(user, level+1)
                        upline_wallet.balance += upline_amount
                        upline_wallet.txnid = generateid()
                        upline_wallet.save()
                        upline_user.wallet += upline_amount
                        upline_user.today_income += upline_amount
                        upline_user.total_income += upline_amount
                        upline_user.progress += upline_amount
                        upline_user.save()
                        upline_user = User.objects.get(username=upline)
                    else:
                        upline_wallet = WalletHistory()   
                        upline_wallet.user_id = upline
                        upline_wallet.amount = upline_amount 
                        upline_wallet.type = "NA"
                        upline_wallet.comment = "{} joined but Level {} not opened!".format(user, level+1)
                        upline_wallet.txnid = generateid()
                        upline_wallet.save()
                        print('else')
                print('outside')
                level = level + 1
            
            model, created = LevelUser.objects.get_or_create(user=userid.username)
            model, created = LevelUser.objects.get_or_create(user=userid.username)
            model.user = userid.username
            model.level = levelp
            model.active = True
            model.direct = user.referral
            model.activated_at = datetime.datetime.now()
            model.save()
            user_id.save()
            message = "Plan purchased"
        else:
            message = "user already joined, please upgrade another ID"
    return message

@staff_member_required
def activation(request, id):
    message = ''

    if request.method == 'POST' and 'delete' in request.POST:
        act = Activation.objects.get(id=id)
        act.delete()
        return redirect('/m2/admin/activations/')

    w = Activation.objects.get(id=id)
    u = User.objects.get(username=w.user)
    if request.method == "POST" and 'action' in request.POST:
        action = request.POST.get('action')
        comment = request.POST.get('comment')
        act_id = request.POST.get('id')
        if action == 'accept':
            act = Activation.objects.get(id=act_id)
            user = act.user
            amount = act.amount
            message = activate(user, amount)
            act.comments = comment
            act.status = 'Approved'
            act.save()
        else:
            act = Activation.objects.get(id=act_id)
            act.comments = comment
            act.status = "Rejected"
            act.save()
        return redirect('/m2/admin/activations/')
    if request.method == "POST" and 'cmnt' in request.POST:
        comment = request.POST.get('comment')
        act_id = request.POST.get('id')
        act = Activation.objects.get(id=act_id)
        act.comments = comment
        act.save()
        return redirect('/m2/admin/activations/')
    return render(request, 'panel/activation.html', {'w': w, 'u': u, 'message': message})

@staff_member_required
def withdrawal(request, id):
    w = Withdrawal.objects.get(id=id)
    u = User.objects.get(username=w.user)
    try:
        k = ImageUploadModel.objects.get(user=w.user)
        b = Paymentoptions.objects.get(user=w.user)
    except Exception as e:
        print(e)
        k = 'blank'
        b = 'blank'
    return render(request, 'panel/withdrawal.html', {'w': w, 'u': u, 'k': k, 'b': b})


@staff_member_required
def orders(request):
    u = Line.objects.all()
    if request.method == 'POST':
        order = request.POST.get('order')
        status = request.POST.get('status')
        comment = request.POST.get('comment')

        model = Order.objects.get(number=int(order))
        if status == 'Cancelled' and model.status != 'Cancelled':
            model.user.shop += 100 + int(model.total_incl_tax)*448/613
            wallet = WalletHistory()
            wallet.user_id = model.user.username
            wallet.amount = 100 + model.total_incl_tax*448/613
            wallet.balance_after = model.user.new_funds + model.user.added_amount + model.user.received_amount + model.user.shopping_wallet + model.user.income + model.user.binary_income
            wallet.type = "credit"
            wallet.comment = "Shopping Refund"
            wallet.txnid = generateid()
            wallet.save()
        model.status = status
        model.comment = comment
        model.save()
    return render(request, 'panel/orders.html', {'u': u})

@staff_member_required
def franchise(request):
    u = Request.objects.all()
    if request.method == 'POST':
        id_ = request.POST.get('id')
        status = request.POST.get('status')
        comment = request.POST.get('comment')

        request_ = Request.objects.get(id=id_)
        amount = request_.amount
        package = Package.objects.get(amount=amount)

        try:
            model = Franchise.objects.get(user=request_.user)
        except Exception as e:
            print(e)
            model = Franchise()
        
        if status == '1':
            model.user = request_.user
            model.wallet += amount
            model.active = 1
            user = User.objects.get(username=request_.user)
            user.new_funds += package.commission_in_percent * package.amount / 100
            user.save()
            wallet = WalletHistory()
            wallet.user_id = model.user
            wallet.amount = amount
            wallet.balance_after = request.user.new_funds + request.user.added_amount + request.user.received_amount + request.user.shopping_wallet + request.user.income + request.user.binary_income
            wallet.type = "credit"
            wallet.comment = "Franchise Wallet Updated"
            wallet.txnid = generateid()
            wallet.save()
            wallet1 = WalletHistory()
            wallet1.user_id = model.user
            wallet1.amount = package.commission_in_percent * package.amount / 100
            wallet1.balance_after = request.user.new_funds + request.user.added_amount + request.user.received_amount + request.user.shopping_wallet + request.user.income + request.user.binary_income
            wallet1.type = "credit"
            wallet1.comment = "Franchise Commission"
            wallet1.save()
            model.save()
        request_.status = status
        request_.comment = comment
        request_.balance_given = amount
        request_.save()
    return render(request, 'panel/franchise.html', {'u': u})

@staff_member_required
def invoice(request, number):
    o = Order.objects.get(number=number)
    l = Line.objects.filter(order__number=number)
    return render(request, 'panel/invoice.html', {'o': o, 'l': l})

class UserProfileView(LoginRequiredMixin, UpdateView):
    fields = [
        "name", "email", "mobile", "nominee", "nominee_relation", "address", "city", "state", "profile_pic",
    ]
    model = User
    template_name = 'panel/profile.html'
    
    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("panel:profile")

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

@login_required
def stores(request):
    if request.method == 'POST':
        store = request.POST.get('store')
        store = Partner.objects.get(id=store)
        try:
            address = PartnerAddress.objects.get(partner__id=store.id)
        except Exception as e:
            print(e)
            address = None
        if 'line1' in request.POST:
            if address == None:
                country = Country.objects.get(iso_3166_1_a2=request.POST.get('country'))
                model = PartnerAddress()
                model.partner = Partner.objects.get(id=store.id)
                store.name = request.POST.get('name')
                model.line1 = request.POST.get('line1')
                model.line2 = request.POST.get('line2')
                model.line3 = request.POST.get('line3')
                model.line4 = request.POST.get('line4')
                model.state = request.POST.get('state')
                model.postcode = request.POST.get('postcode')
                model.country = country
                model.save()
                store.save()
                store = Partner.objects.filter(Q(users__id=request.user.id) | Q(admin_user__id=request.user.id)).distinct()
                return render(request, 'panel/stores.html', {'stores': store})
            if address != None:
                model = address
                country = Country.objects.get(iso_3166_1_a2=request.POST.get('country'))
                store.name = request.POST.get('name')
                model.line1 = request.POST.get('line1')
                model.line2 = request.POST.get('line2')
                model.line3 = request.POST.get('line3')
                model.line4 = request.POST.get('line4')
                model.state = request.POST.get('state')
                model.postcode = request.POST.get('postcode')
                model.country = country
                model.save()
                store.save()
                store = Partner.objects.filter(Q(users__id=request.user.id) | Q(admin_user__id=request.user.id)).distinct()
                return render(request, 'panel/stores.html', {'stores': store})
        if 'staff_username' in request.POST:
            store.users.add(User.objects.get(username=request.POST.get('staff_username')))
            store.save()
            store = Partner.objects.filter(Q(users__id=request.user.id) | Q(admin_user__id=request.user.id)).distinct()
            return render(request, 'panel/stores.html', {'stores': store})
        if 'remove_user' in request.POST:
            store.users.remove(User.objects.get(username=request.POST.get('remove_user')))
            store.save()
            store = Partner.objects.filter(Q(users__id=request.user.id) | Q(admin_user__id=request.user.id)).distinct()
            return render(request, 'panel/stores.html', {'stores': store})
        if 'make_admin' in request.POST:
            store.admin_user = User.objects.get(username=request.POST.get('make_admin'))
            store.save()
            store = Partner.objects.filter(Q(users__id=request.user.id) | Q(admin_user__id=request.user.id)).distinct()
            return render(request, 'panel/stores.html', {'stores': store})
        return render(request, 'panel/store-edit.html', {'store': store, 'address': address})
    user = request.user
    store = Partner.objects.filter(Q(users__id=request.user.id) | Q(admin_user__id=request.user.id)).distinct()
    return render(request, 'panel/stores.html', {'stores': store})

@login_required
def neft(request):
    message = ""
    withdrawals = Withdrawal.objects.filter(user=request.user.username)

    if request.method == 'POST':
        user_id = request.user
        amount = float(request.POST.get('amount'))
        try:
            if True:
                if request.user.new_funds >= amount and request.user.redeem_access == False:
                    if amount%500 == 0:
                        user_id.new_funds = user_id.new_funds - amount
                        amount = float(request.POST.get('amount'))
                        model = Withdrawals()
                        model.user = user
                        model.amount = amount
                        model.status = 'pending'
                        model.description = ''
                        model.total_amount = amount*95/100
                        model.admin_fees = 0
                        model.tax = amount*5/100

                        userwallet = WalletHistory()
                        userwallet.balance_after = userbal - amount
                        userwallet.user_id = str(user_id)
                        userwallet.amount = float(amount)
                        userwallet.type = "debit"
                        userwallet.filter = "NEFT"
                        userwallet.comment = "NEFT"

                        userwallet.txnid = generateid()
                        userwallet.save()
                        user_id.save()
                        model.save()
                        message = "NEFT Request Received!".format(amount, bank)
                    else:
                        message = "Please Enter Amount in multiples of 500!"
                else:
                    message = "Something went wrong"
            else:
                message = "NEFT Services, not started yet"
        except Exception as e:
            print(e)
            message = "Error 500 {}".format(e)

    return render(request, 'panel/neft.html', {'message': message, 'withdrawals': withdrawals})

def guestlogin(request):
    """Log in a user without requiring credentials with user object"""
    if request.method == 'POST':
        user = request.POST.get('username')
        user = User.objects.get(username=user)
    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
    return redirect('/users/')


def wallets(request):
    return render(request, 'panel/wallets.html', {})

def active(request):
    return render(request, 'panel/active.html', {})

def today(request):
    return render(request, 'panel/today.html', {})

def date(request):
    return render(request, 'panel/date.html', {})

def pending(request):
    return render(request, 'panel/pending.html', {})

def autopool(request):
    return render(request, 'panel/autopool.html', {})

def rank(request):
    return render(request, 'panel/rank.html', {})

def royalty(request):
    return render(request, 'panel/royalty.html', {})

def cto(request):
    return render(request, 'panel/cto.html', {})

def income(request):
    return render(request, 'panel/income.html', {})