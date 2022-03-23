from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from library.models import User, TypeOfSport

# Ajax request for user data
class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'phone', 'kota_kab', 'sport_pref', 'photo']

class UserView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            serializer = UserSerializer(user)

            return JsonResponse(serializer.data, safe=False)

        except:
            return Response({ 'error': 'Something went wrong when retrieving profile' })


# Changing user data
class ChangeProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user

        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            data = self.request.data

            if 'name' in data:
                name = data['name']
                user.name = name

            if 'phone' in data:    
                phone = data['phone']
                user.phone = phone
            
            if 'kota_kab' in data: 
                kota_kab = data['kota_kab']
                user.kota_kab = kota_kab
            
            if 'sport_pref' in data: 
                sport_pref = data['sport_pref']

                try:
                    user.sport_pref = TypeOfSport.objects.get(code=sport_pref)
                except:
                    return Response({ 'success': 0, 'message': 'Sport code does not exist' })

            try:
                user.save()

                return Response({ 'success': 1, 'message': 'User profile has been updated' })
            
            except:
                return Response({ 'success': 0, 'message': 'Something went wrong when updating user data' })


# Changing username
class ChangeUsernameView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
        
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            try:
                data = self.request.data
                username = data['username']

                if user.username is not None :
                    return Response({ 'success': 0, 'message': 'Username has been set' })
                else:
                    if User.objects.filter(username=username).exists():
                        return Response({ 'success': 0, 'message': 'Username has been used' })
                    else:
                        try:
                            user.username = username
                            user.save()

                            return Response({ 'success': 1, 'message': 'Username has been updated' })

                        except:
                            return Response({ 'success': 0, 'message': 'Something went wrong when updating username' })

            except:
                return Response({ 'success': 0, 'message': 'Data is incomplete' })


# Changing email
class ChangeEmailView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
        
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            try:
                data = self.request.data
                email = data['email']

                if User.objects.filter(email=email).exists():
                    return Response({ 'success': 0, 'message': 'Email has been used' })
                else:
                    try:
                        user.email = email
                        user.save()

                        return Response({ 'success': 1, 'message': 'Email has been updated' })

                    except:
                        return Response({ 'success': 0, 'message': 'Something went wrong when updating user email' })

            except:
                return Response({ 'success': 0, 'message': 'Data is incomplete' })


# Changing passward
class PasswordValidation(APIView):
    def post(self, request, format=None):
        try:
            user = self.request.user
        
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            try:
                password = request.data['password']
            except:
                return Response({ 'success': 0, 'message': 'Data is incomplete' })
            else:
                try:
                    valid = authenticate(email=user.email, password=password)

                    if valid is not None:
                        return Response({ 'success': 1, 'message': 'Password is valid' })
                    else:
                        return Response({ 'success': 0, 'message': 'Password is invalid' })

                except:
                    return Response({ 'success': 0, 'message': 'Something went wrong when authenticating user' })


class ChangPasswordView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
        
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            try:
                data = self.request.data
                password1 = data['password1']
                password2 = data['password2']

                if password1 == password2:
                    try:
                        validate_password(password1, user)

                        try:
                            user.set_password(password1)
                            user.save()

                            return Response({ 'success': 1, 'message': 'Password has been updated' })
                        except:
                            return Response({ 'success': 0, 'message': 'Something went wrong when updating user password' })

                    except ValidationError as error:
                        return Response({ 'success': 0, 'message': error })

                else:
                    return Response({ 'success': 0, 'message': 'Passwords does not match' })

            except:
                return Response({ 'success': 0, 'message': 'Data is incomplete' })

# Changing photo profile
class UserPhotoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['photo']

    def save(self, *args, **kwargs):
        if self.instance.photo:
            self.instance.photo.delete()
        return super().save(*args, **kwargs)

class ChangePhotoView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, format=None):
        try:
            user = self.request.user
        
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            serializer = UserPhotoSerializer(data=request.data, instance=user)
            if serializer.is_valid():
                serializer.save()

                photo = serializer.data['photo']

                return Response({ 'success': 1, 'message': 'User photo has been uploaded',  'photo': photo})
            else:
                return Response({ 'success': 0, 'message': 'Something went wrong when uploading user photo' })