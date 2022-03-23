from django.urls import path

from .views import *

urlpatterns = [
    path('my_bills/', MyBills.as_view(), name='my_bills'),
    path('my_booking/', MyBooking.as_view(), name='my_booking'),
    path('order_history/', OrderHistory.as_view(), name='order_history'),
    path('booking_receipt/', GetBookingReceipt.as_view(), name='booking_receipt'),
]