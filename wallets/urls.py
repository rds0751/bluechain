from django.conf.urls import url
from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    url(r"^transesdxfcgvhbfer/$", views.transfer, name="transfer"),
    url(r"^fund-request/$", views.fundrequest, name="fundrequest"),
    url(r"^history/$", views.history, name="history"),
    url(r"^pool/$", views.pool, name="pool"),
    url(r"^level/$", views.level, name="level"),
    url(r"^rewards/$", views.rewards, name="rewards"),
    url(r"^referral/$", views.referral, name="referral"),
    url(r"^royalty/$", views.royalty, name="royalty"),
    url(r"^rank/$", views.rank, name="rank"),
    url(r"^roi/$", views.roi, name="roi"),
    url(r"^direct/$", views.direct, name="direct"),
    url(r"^passive/$", views.passive, name="passive"),
    url(r"^community/$", views.community, name="community"),
    url(r"^staking/$", views.staking, name="staking"),
    url(r"^royalty1/$", views.royalty1, name="royalty1"),
    url(r"^booster/$", views.booster, name="booster"),
    url(r"^community/$", views.community, name="community"),
    url(r"^transfer/$", views.imps, name="imps"),
    url(r"^send/$", views.send, name="send"),
    url(r"^account/$", views.paymentoptions, name="account"),
    url(r"^mt5-transfer/$", views.mt5t, name="neft"),
    url(r"^recharge/callback/$", views.callback, name="callback"),
    url(r"^cancel/(?P<id>[\w.@+-]+)/$", views.cancel_neft, name="cancel"),
    url(r"^confirm/(?P<id>[\w.@+-]+)/$", views.confirm_neft, name="confirm"),
    url(r"^cancel-generate/(?P<id>[\w.@+-]+)/$", views.cancel_generate, name="cancel-generate"),
    url(r"^confirm-generate/(?P<id>[\w.@+-]+)/$", views.confirm_generate, name="confirm"),
    url(r"^withdrawDollarVridhi/$", views.withdrawDollarVridhi, name="confirm"),
    path("otp/",views.DollarVridhi_verification,name="send otp"),
    path("verify_metamask_txn/",views.verify_metamask_txn,name="verify_metamask_txn"),
]

