from django.urls import path

from .views.home import *
from .views.search import *
from .views.update_db import *
from .views.test import *

urlpatterns = [
    # Home
    path('', home, name='home'),

    # Search
    path('ctg/<str:category>/', category, name='category'),
    path('search/', search, name='search'),

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

    # Test
    path('sending_email/', sending_email, name='sending_email'),
    path('send_notif/', send_notif, name='send_notif'),
]