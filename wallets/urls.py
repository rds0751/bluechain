from django.conf.urls import url
from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    url(r"^transesdxfcgvhbfer/$", views.transfer, name="transfer"),
    url(r"^fund-request/$", views.fundrequest, name="fundrequest"),
    url(r"^history/$", views.history, name="history"),
    url(r"^cto/$", views.cto, name="history"),
    url(r"^direct/$", views.direct, name="history"),
    url(r"^level/$", views.referral, name="history"),
    url(r"^sponsor/$", views.sponsor, name="history"),
    url(r"^pool/$", views.pool, name="history"),
    url(r"^transfer/$", views.imps, name="imps"),
    url(r"^send/$", views.send, name="send"),
    url(r"^account/$", views.paymentoptions, name="account"),
    url(r"^mt5-transfer/$", views.mt5t, name="neft"),
    url(r"^recharge/callback/$", views.callback, name="callback"),
    url(r"^cancel/(?P<id>[\w.@+-]+)/$", views.cancel_neft, name="cancel"),
    url(r"^confirm/(?P<id>[\w.@+-]+)/$", views.confirm_neft, name="confirm"),
    url(r"^cancel-generate/(?P<id>[\w.@+-]+)/$", views.cancel_generate, name="cancel-generate"),
    url(r"^confirm-generate/(?P<id>[\w.@+-]+)/$", views.confirm_generate, name="confirm"),
    path("send_otp/",views.send_otp,name="send otp"),
]