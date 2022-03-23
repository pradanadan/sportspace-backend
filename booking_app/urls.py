from django.urls import path

from .views import *

urlpatterns = [
    path('', BookingView.as_view(), name='booking'),
    path('payment_cd/', PaymentCDView.as_view(), name='payment_cd'),
    path('payment_confirm/', PaymentConfirmView.as_view(), name='payment_confirm'),
]