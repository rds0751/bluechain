# -*- coding: utf-8 -*-
from django.conf.urls import url

from cryptopay import views

app_name = 'cryptopay'
urlpatterns = [

    url(
        # regex="^payment/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$",
        regex="^payment/$",
        view=views.CryptoPaymentDetailView.as_view(),
        name='crypto_payment_detail',
    ),

]
