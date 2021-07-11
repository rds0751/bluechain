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
from kyc.models import ImageUploadModel
import random

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
	ci = 0
	co = 0
	tre = 0
	for wh in wwhs:
		if 'Shopping Wallet Topup' in wh.comment or 'spent binary id' in wh.comment:
			ci += wh.amount
		elif 'NEFT' in wh.comment or 'imps' in wh.comment or 'spent on recharge' in wh.comment:
			co += wh.amount
	for wh in dwhs:
		if 'Shopping Wallet Topup' in wh.comment or 'spent binary id' in wh.comment:
			tre += wh.amount
	return render(request, 'panel/home.html', {'ci': ci, 'co': co, 'tre':tre  })

@staff_member_required
def users(request):
	q = 'blank'
	s = 'blank'
	r = 100
	u = User.objects.all().order_by('?')[:100]
	if request.method == 'POST' and request.POST.get('r') != '':
		q = request.POST.get('q')
		s = request.POST.get('s')
		r = request.POST.get('r')
		u = User.objects.all().order_by('?')[:int(r)]
		if 'q' in request.POST and len(request.POST.get('q'))>=4:
			u = User.objects.filter(username__icontains=request.POST.get('q'))
			s = 'blank'
		if request.POST.get('s') != 'blank':
			u = User.objects.all().annotate(on_hold=Sum(F('income') + F('binary_income') + F('added_amount') + F('received_amount'))).order_by('-'+request.POST.get('s'))[:int(request.POST.get('r'))]
			q = 'blank'
		if 'q' in request.POST and request.POST.get('s') != 'blank' and len(request.POST.get('q'))>=3:
			u = User.objects.filter(username__icontains=request.POST.get('q')).annotate(on_hold=Sum(F('income') + F('binary_income') + F('added_amount') + F('received_amount'))).order_by('-'+request.POST.get('s'))
	return render(request, 'panel/users.html', {'u': u, 'q': q, 's': s, 'r': r})

@staff_member_required
def withdrawals(request):
	w = Withdrawals.objects.all()
	return render(request, 'panel/withdrawals.html', {'w': w})

@staff_member_required
def withdrawal(request, id):
	w = Withdrawals.objects.get(id=id)
	u = User.objects.get(username=w.user)
	try:
		k = ImageUploadModel.objects.get(user=w.user)
		b = Paymentoptions.objects.get(user=w.user)
	except Exception as e:
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
    withdrawals = Withdrawals.objects.filter(user=request.user.username)

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
            message = "Error 500 {}".format(e)

    return render(request, 'panel/neft.html', {'message': message, 'withdrawals': withdrawals})

def guestlogin(request):
    """Log in a user without requiring credentials with user object"""
    if request.method == 'POST':
    	user = request.POST.get('login')
    	user = User.objects.get(username=user)
    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
    return redirect('/users/')