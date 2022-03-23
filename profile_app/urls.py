from django.urls import path

from .views import *

urlpatterns = [
    path('get_user_data/', UserView.as_view(), name='user_data'),
    path('change_profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('change_username/', ChangeUsernameView.as_view(), name='change_username'),
    path('password_validation/', PasswordValidation.as_view(), name='password_validation'),
    path('change_password/', ChangPasswordView.as_view(), name='change_password'),
    path('change_photo/', ChangePhotoView.as_view(), name='change_photo'),
]