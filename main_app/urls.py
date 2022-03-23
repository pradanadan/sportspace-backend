from django.urls import path

from .views.home import *
from .views.search import *

urlpatterns = [
    # Home
    path('home/get_rec_1/', get_rec_1, name='get_rec_1'),
    path('home/get_rec_2/', get_rec_2, name='get_rec_2'),
    path('home/get_article/', get_article, name='get_article'),

    # Search
    path('search/', search, name='search'),
]