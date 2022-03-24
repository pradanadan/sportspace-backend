from django.urls import path

from .views.update_db import *

urlpatterns = [
    # Updating database
    path('update_db/', update_db, name='update_db'),
    path('type_sport/', type_sport, name='type_sport'),
    path('book_dict/', book_dict, name='book_dict'),
    path('kecamatan/', kecamatan, name='kecamatan'),
    path('user_partner/', user_partner, name='user_partner'),
    path('court/', court, name='court'),
    path('article/', article, name='article'),
    path('booking/', booking, name='booking'),
    path('booking_hours/', booking_hours, name='booking_hours'),
]