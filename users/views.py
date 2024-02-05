from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import permissions, status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, BlacklistedToken
from templated_mail.mail import BaseEmailMessage
from smtplib import SMTPSenderRefused
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import timedelta

User = get_user_model()

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

# ----------- jwt auth -------------

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            
            if user:
                return Response({"created": "Аккаунт успешно создан"}, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAvatar(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAvatarSerializer
    permission_classes = (IsAuthenticated,)
    

class UserChangePassword(generics.UpdateAPIView):
    model = User

    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"error": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response({"status": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------
#СБРОС ПАРОЛЯ ПО ПОЧТЕ

@api_view(['POST'])
@permission_classes([AllowAny])
def sendToEmailResetPassword(request):
    try:
        if request.method == 'POST':
            serializer = SendResetPasswordToEmailSerializer(data=request.data)

            if serializer.is_valid():
                email = serializer.data.get('email')
                user = User.objects.get(email=email)

                if user:
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token).replace('.', '–')
                    
                    send_mail('〽 СБРОС ПАРОЛЯ', None, settings.EMAIL_HOST_USER, [email], fail_silently=False, html_message=render_to_string('reset_password.html', {'email': email, 'protocol': 'http', 'domain': settings.DOMAIN, 'token': token}))

                    # BaseEmailMessage(context={'token': refresh.access_token}, template_name='reset_password.html').send(to=[email])

                return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
        

class UserResetPassword(generics.UpdateAPIView):
    model = User

    serializer_class = UserResetPasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = UserResetPasswordSerializer(data=request.data)

        if serializer.is_valid():  
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
























































# ------------- session auth -------------

# class UserLogin(APIView):
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = (SessionAuthentication,)

#     def post(self, request):
#         data = request.data
#         assert validate_email(data)
#         assert validate_password(data)
#         serializer = UserLoginSerializer(data=data)
        
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.check_user(data)
#             login(request, user)
#             return Response(serializer.data, status=status.HTTP_200_OK)


# class UserLogout(APIView):
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = ()
    
#     def post(self, request):
#         logout(request)
#         return Response(status=status.HTTP_200_OK)


# class UserView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication,)
    
#     def get(self, request):
#         serializer = UserAvatarSerializer(request.user, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)