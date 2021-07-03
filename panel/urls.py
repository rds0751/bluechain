from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import re_path

from . import views

app_name = "panel"
urlpatterns = [
    url(r'^', views.home, name='home'),
    url(r'^login/$', views.guestlogin, name='guestlogin'),
    url(r'^stores/$', views.stores, name='stores'),
    url(r'^users/$', views.users, name='users'),
    url(r'^~withdrawals/$', views.neft, name='neft'),
    url(r'^withdrawals/$', views.withdrawals, name='withdrawals'),
    url(r'^withdrawals/(?P<id>[\w.@+-]+)/$', views.withdrawal, name='withdrawal'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^invoice/(?P<number>[\w.@+-]+)/$', views.invoice, name='invoice'),
    url(regex=r"^~profile/$", view=views.UserProfileView.as_view(), name="profile"),
    url(r'^franchise/$', views.franchise, name='franchise'),
]