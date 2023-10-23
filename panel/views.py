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
from home.models import Company

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
    if request.method == "POST" and 'hold' in request.POST:
        user = User.objects.get(id=id)
        if user.is_active:
            user.whold = False
        else:
            user.whold = True
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
    w = WalletHistory.objects.filter(comment__icontains="Sent to your wallet")
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

from wallets.models import FundRequest
@staff_member_required
def frs(request):
    w = FundRequest.objects.all().order_by('-created_at')
    for x in w:
        try:
            x.user = User.objects.get(username=x.user)
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
        
        ccm = 0
        
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

    user = User.objects.get(username=user)
    upline_user = user.referral
    packamount = amount
    levelp = LevelIncomeSettings.objects.get(amount=packamount)
    user_id = User.objects.get(username=str(user))
    userjoined = userjoined(user)
    print(userjoined)
    if True:
        if True:
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
            'level1': 2/100, 
            'level2': 2/100,
            'level3': 2/100,
            'level4': 2/100,
            'level5': 2/100,
            }

            level = 0   
            upline_user = userid.referral    
            userid = user   
            amount = packamount 
            uplines = [upline_user, ]
            while level < 4 and upline_user != 'blank':
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
                    upgraded = LevelUser.objects.get(user='DV111111')
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
                    print(directs.count(), upline_user, '-----------------------------------------------------------------------------')

                    if direct:
                        if directs.count() < 2 and upline_user.total_income + 25 <= 400: 
                            upline_wallet = WalletHistory()
                            upline_wallet.user_id = upline
                            upline_wallet.amount = 25
                            upline_wallet.type = "credit"
                            upline_wallet.comment = "Direct Income for AB nodes by {}".format(user)
                            upline_wallet.balance += 25
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            upline_user.wallet += 25
                            upline_user.today_income += 25
                            upline_user.direct_income += 25
                            upline_user.total_income += 25
                            upline_user.save()
                        if directs.count() < 2:
                            upline_user = User.objects.get(username=upline)
                            userx = upline_user.username
                            x = True
                            print(userx, 'ewsdrtfgyhujikoijuhgytfdresdrftgyhjkm')
                            while x:
                                try:
                                    new_upline_user = User.objects.get(
                                        username=User.objects.get(username=userx)
                                        )
                                except Exception as e:
                                    x = False
                                try:
                                    w = WalletHistory.objects.get(comment="Direct Income from Non-AB nodes by "+userx)
                                    print(userx)
                                    print(w.comment)
                                    new_upline_user = username=User.objects.get(username=new_upline_user.referral)
                                    x = False
                                    if new_upline_user.total_income + 25 <= 400:
                                        new_upline_wallet = WalletHistory()
                                        new_upline_wallet.user_id = new_upline_user.username
                                        new_upline_wallet.amount = 25
                                        new_upline_wallet.type = "credit"
                                        new_upline_wallet.comment = "Diamond Income for AB nodes by {}".format(user)
                                        new_upline_wallet.balance += 25
                                        new_upline_wallet.txnid = generateid()
                                        new_upline_wallet.save()
                                        new_upline_user.wallet += 25
                                        new_upline_user.today_income += 25
                                        new_upline_user.diamond_income += 25
                                        new_upline_user.total_income += 25
                                        new_upline_user.progress += 25
                                        new_upline_user.save()
                                except Exception as e:
                                    print(str(e))
                                    userx = new_upline_user.referral
                                print(userx, new_upline_user, new_upline_user.referral, 'loooooooooooooooooooooooop')
                                if not userx:
                                    print(userx, 'not userx')
                                    x = False
                                
                        if directs.count() >= 2 and upline_user.total_income + 50 <= 400:
                            upline_wallet = WalletHistory()
                            upline_wallet.user_id = upline
                            upline_wallet.amount = 50
                            upline_wallet.type = "credit"
                            upline_wallet.comment = "Direct Income from Non-AB nodes by {}".format(user)
                            upline_wallet.balance += 50
                            upline_wallet.txnid = generateid()
                            upline_wallet.save()
                            upline_user.wallet += 50
                            upline_user.today_income += 50
                            upline_user.direct_income += 50
                            upline_user.total_income += 50
                            upline_user.direct_income += 50
                            upline_user.save()
                            upline_user = User.objects.get(username=upline)
                    if True:
                        upline_amount = levels['level{}'.format(level+1)]*amount
                        upline_wallet = WalletHistory()
                        upline_wallet.user_id = upline
                        upline_wallet.amount = upline_amount
                        upline_wallet.type = "credit"
                        upline_wallet.comment = "New Upgrade by {} in level {}".format(
                            user, 
                            level+1
                            )
                        upline_wallet.balance += upline_amount
                        upline_wallet.txnid = generateid()
                        upline_wallet.save()
                        upline_user.wallet += upline_amount
                        upline_user.today_income += upline_amount
                        upline_user.total_income += upline_amount
                        upline_user.progress += upline_amount
                        upline_user.level_income += upline_amount
                        upline_user.save()
                        upline_user = User.objects.get(username=upline)
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
            user_id.total_business = 0
            user_id.save()
            c = Company.objects.get(id=1)
            c.total_turnover += 100
            c.today_new_ids += 1
            c.today_turnover += 100
            c.save()
            message = "Plan purchased"
        else:
            message = "user already joined please upgrade another ID"
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