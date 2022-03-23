from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime

from .user import *
from .court import *


class BookHoursDict(models.Model):
    hour_start = models.TimeField()
    hour_end = models.TimeField()

    def __str__(self):
        string = str(self.hour_start) + ' - ' + str(self.hour_end)
        return string

class BookingStatusCatalog(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.status_name

class PaymentMethod(models.Model):
    code = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Booking deadline calculation
def one_hour_hence():
    return timezone.now() + timezone.timedelta(hours=1)

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    user_partner = models.ForeignKey(UserPartner, on_delete=models.PROTECT)
    court = models.ForeignKey(Court, on_delete=models.PROTECT)
    date_book = models.DateField()
    lunas = models.BooleanField()
    price = models.BigIntegerField()
    unique_price = models.BigIntegerField()
    method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    status = models.ForeignKey(BookingStatusCatalog, on_delete=models.PROTECT, default=1)
    ts_created = models.DateTimeField(default=timezone.now)
    payment_dl = models.DateTimeField(default=one_hour_hence)
    active = models.BooleanField(default=True)

    def cancellation(self):
        now = datetime.now()
        if (now > self.payment_dl) and self.status.status_name=='unpaid':
            self.active = False
            self.save()

class BookingHours(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    book_hours = models.ForeignKey(BookHoursDict, on_delete=models.PROTECT)

class BookingStatusEvent(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    status = models.ForeignKey(BookingStatusCatalog, on_delete=models.PROTECT)
    ts_created = models.DateTimeField(default=timezone.now)

class PaymentConfirm(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    bukti = models.ImageField(upload_to='images/payments/', max_length=500)
    read = models.BooleanField(default=False)