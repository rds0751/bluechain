from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import re_path

from . import views

app_name = "panel"
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.guestlogin, name='guestlogin'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<id>[\w.@+-]+)/$', views.user, name='users'),
    url(r'^~withdrawals/$', views.neft, name='neft'),
    url(r'^withdrawals/$', views.withdrawals, name='withdrawals'),
    url(r'^ids/$', views.ids, name='ids'),
    url(r'^bankdetails/$', views.bankdetails, name='bankdetails'),                  
    url(r'^kycs/$', views.kycs, name='kycs'),
    url(r'^activations/$', views.activations, name='activations'),   
    url(r'^frs/$', views.frs, name='frs'),                  
    url(r'^activations/(?P<id>[\w.@+-]+)/$', views.activation, name='activation'),  
    url(r'^withdrawals/(?P<id>[\w.@+-]+)/$', views.withdrawal, name='withdrawal'),  
    url(regex=r"^~profile/$", view=views.UserProfileView.as_view(), name="profile"),
    
    url(r'^wallets/', views.wallets, name="wallets"),
    url(r'^active/', views.active, name="active"),
    url(r'^today/', views.today, name="today"),
    url(r'^date/', views.date, name="date"),
    url(r'^withdrawal/', views.withdrawal, name="withdrawal"),
    url(r'^pending/', views.pending, name="pending"),
    url(r'^autopool/', views.autopool, name="autopool"),
    url(r'^rank/', views.rank, name="rank"),
    url(r'^royalty/', views.royalty, name="royalty"),
    url(r'^cto/', views.cto, name="cto"),
    url(r'^income/', views.income, name="income"),
] 