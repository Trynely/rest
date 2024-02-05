from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import views as auth_views
from one.models import *

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['img'] = "http://127.0.0.1:8000/media/" + str(user.img)

        return token

    
class SendResetPasswordToEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
#--------------------------------------------------------------------------

# user avatar

class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['img']

# user register

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user

# user change password
    
class UserChangePasswordSerializer(serializers.Serializer):
    model = User
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserResetPasswordSerializer(serializers.Serializer):
    model = User
    
    new_password = serializers.CharField(required=True)




















# ---------------------- session auth ----------------------------

# user login

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
    
#     def check_user(self, clean_data):
#         user = authenticate(username=clean_data['email'], password=clean_data['password'])
        
#         if not user:
#             raise ValidationError('user not found')
#         return user
    
# -----------------------------------------------------------------