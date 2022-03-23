from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class TypeOfSport(models.Model):
    code = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    kota_kab = models.CharField(max_length=200, null=True, blank=True)
    sport_pref = models.ForeignKey(TypeOfSport, on_delete=models.PROTECT, null=True, blank=True)
    photo = models.ImageField(upload_to='images/users/', null=True, blank=True, max_length=500)
    date_joined  = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class CityList(models.Model):
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.city

class KecamatanList(models.Model):
    city = models.ForeignKey(CityList, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserPartner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True) # Still need to be filled after sign up
    phone = models.CharField(max_length=200, null=True, blank=True)
    venue_name = models.CharField(max_length=200, null=True, blank=True) # Still need to be filled after sign up
    address = models.CharField(max_length=200, null=True, blank=True) # Still need to be filled after sign up
    city = models.ForeignKey(CityList, on_delete=models.PROTECT, null=True, blank=True) # Still need to be filled after sign up
    kecamatan = models.ForeignKey(KecamatanList, on_delete=models.PROTECT, null=True, blank=True) # Still need to be filled after sign up
    op_hours_start = models.TimeField(default='09:00') # Still need to be changed after sign up
    op_hours_end = models.TimeField(default='21:00') # Still need to be changed after sign up

    longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    
    photo = models.ImageField(upload_to='images/partners/', null=True, blank=True, max_length=500)
    ts_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class KPI(models.Model):
    user_partner = models.OneToOneField(UserPartner, on_delete=models.CASCADE)
    book_s = models.IntegerField(null=True, blank=True)
    book_f = models.IntegerField(null=True, blank=True)
    confirm_t = models.TimeField(null=True, blank=True)