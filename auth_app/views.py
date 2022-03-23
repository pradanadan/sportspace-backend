from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from .token import *
from .forms.signupLoginForm import SignupForm
from library.models.user import User

class IsLoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            user = self.request.user

            try:
                isAuthenticated = user.is_authenticated

                if isAuthenticated:
                    print('masuk isauthenticated')
                    return Response({ 'is_login': True })
                else:
                    print('gagal isauthenticated')
                    return Response({ 'is_login': False })
            except:
                print('error')
                return Response({ 'error': 'Something went wrong when checking login status' })
        except:
            print('masuk except')
            return Response({ 'is_login': False })


@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        email = data['email']

        try:
            form = SignupForm(data)

            if form.is_valid():
                user = form.save(commit=False)
                user.save()

                # Mail System
                current_site = get_current_site(request)
                mail_subject = 'Aktivasi Akun'
                message = render_to_string('auth_app/email/activation_user.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()

                return Response({ 'success': 1, 'message': 'User created successfully' })
            
            else:
                return Response({ 'success': 0, 'message': form.errors })

        except:
                return Response({ 'success': 0, 'message': 'Something went wrong when registering account' })


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Terimakasih telah mengkonfirmasi email Anda. Sekarang Anda bisa login dengan akun Anda.')
    else:
        return HttpResponse('Tautan aktivasi tidak sah!')


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        email = data['email']
        password = data['password']

        try:
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return Response({ 'success': 'User authenticated' })
            else:
                return Response({ 'error': 'Error Authenticating' })
        except:
            return Response({ 'error': 'Something went wrong when logging in' })


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            logout(request)
            print('melewati logout')
            return Response({ 'success': 'Loggout Out' })
        except:
            print('gagal logout')
            return Response({ 'error': 'Something went wrong when logging out' })