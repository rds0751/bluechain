from allauth.account.forms import SignupForm
from django import forms
from .models import *
import random
import requests
from level.models import LevelUser, LevelIncomeSettings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class SimpleSignupForm(SignupForm):
	mobile = forms.CharField(max_length=250, label='mobile')
	name = forms.CharField(max_length=250, label='name')
	referal_code = forms.CharField(max_length=14, label="refer")

	def get_success_url(self):
		return '/signup/onboarding/'
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', 'mobile')

	def clean_name(self):
		name = self.cleaned_data['name']
		return name[0].upper() + name[1:].lower()

	def clean_username(self):
		def generateuser():
			r = random.randint(100001,999999)
			u = User.objects.filter(username='DV{}'.format(r)).count()
			if u > 0:
				generateuser()
			else:
				return 'DV{}'.format(r)
		u = generateuser()
		username = u
		return username

	def save(self, request):
		user = super(SimpleSignupForm, self).save(request)
		referral = self.cleaned_data['referal_code'].upper()
		try:
			userr = User.objects.get(username=referral)
		except Exception as e:
			userr = 'blank'
		if userr == 'blank':
			referral = 'DV111111'
		plan = LevelUser()
		plan.user = user
		plan.level = LevelIncomeSettings.objects.get(id=1)
		plan.active = False
		plan.left_months = 0
		plan.direct = referral
		plan.save()
		user.mobile = self.cleaned_data['mobile']
		user.name = self.cleaned_data['name']
		user.referral = referral
		user.visiblepass = self.cleaned_data['password1']
		user.save()
		return user