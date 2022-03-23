from django.urls import path

from .views.court import *
from .views.favorite_court import *

urlpatterns = [
    # Court
    path('<str:user_partner>/<slug:slug>/', CourtDetailView.as_view(), name='court_detail'),
    path('<str:user_partner>/<slug:slug>/check/', check, name='court_date'),

    # Favorite Court
    path('favorite_court/', FavCourtView.as_view(), name='favorite_court'),
    path('get_favorite_court/', GetFavCourtView.as_view(), name='get_favorite_court'),
]