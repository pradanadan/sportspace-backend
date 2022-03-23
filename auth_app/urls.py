from django.urls import path

from .views import *
from .get_csrf import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('is_login/', IsLoginView.as_view(), name='is_login'),
    path('get_csrf/', GetCsrf.as_view(), name='csrf'),
]