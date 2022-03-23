from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify

from .user import *

# Create your models here.

class Court(models.Model):
    user_partner = models.ForeignKey(UserPartner, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    type = models.ForeignKey(TypeOfSport, on_delete=models.PROTECT)
    rate = models.BigIntegerField()
    dp = models.BigIntegerField()
    ROOMS = [('indoor', 'Indoor'),
                ('outdoor', 'Outdoor')]
    room = models.CharField(max_length=100, choices=ROOMS, null=True, blank=True)
    floor = models.CharField(max_length=200, null=True, blank=True)
    loker = models.BooleanField(default=False)
    ruang_ganti = models.BooleanField(default=False)
    shower_room = models.BooleanField(default=False)
    deskripsi = models.TextField(null=True, blank=True)
    img1 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img2 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img3 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img4 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img5 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img6 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img7 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img8 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img9 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    img10 = models.ImageField(upload_to='images/courts/', blank=True, null=True, max_length=500)
    n_book = models.IntegerField(default=0)
    ts_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('court_detail', kwargs={'user_partner': self.user_partner, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class FavCourt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
        