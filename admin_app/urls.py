from django.urls import path

from .views import *

urlpatterns = [
    path('payment/', PaymentConfirmList.as_view(), name='admin_payment'),
    path('booking_detail/', BookingDetail.as_view(), name='admin_booking_detail'),
    path('validate_payment/', PaymentValidationView.as_view(), name='validate_payment'),
    path('send_receipt/', SendBookingReceipt.as_view(), name='send_receipt'),
]