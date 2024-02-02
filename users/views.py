import json
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from one.models import Things
from rest_framework.response import Response
from .serializers import *
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, BlacklistedToken
from templated_mail.mail import BaseEmailMessage
from django.core.exceptions import ObjectDoesNotExist
from smtplib import SMTPSenderRefused
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()

# ----------- jwt auth -------------

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
 

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


@api_view(['POST'])
@permission_classes([AllowAny])
def getJwtTokenWithoutPassword(request):
    if request.method == 'POST':
        serializer = SendResetPasswordToEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)

    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}) 


@api_view(['GET'])
@permission_classes([AllowAny])
def getJwtTokenWithoutPassword_2(request):
    user = User.objects.get(email='tagirramaz727@gmail.com')
    
    access_token = AccessToken.for_user(user=user)
    refresh_token = RefreshToken.for_user(user=user)

    return Response({'access': str(access_token), 'refresh': str(refresh_token)})


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



class Test(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        x = {"textd": "dq1dw21d"}

        return Response(x)

        # if serializer.is_valid(raise_exception=True):     
        #     return Response(serializer.data)
         
            
class TestModel(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        objects = User.objects.all()
        serializer = TestModelSerializer(objects, many=True)

        for x in serializer.data:
            for l in x:
                print(x[l])
        return Response(serializer.data)

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
                    token = str(refresh.access_token).replace('.', '-')
                    
                    send_mail('〽 СБРОС ПАРОЛЯ', None, settings.EMAIL_HOST_USER, [email], fail_silently = False, html_message = render_to_string('reset_password.html', {'email': email, 'protocol': 'http', 'domain': settings.DOMAIN, 'token': token}))

                    # BaseEmailMessage(context={'token': refresh.access_token}, template_name='reset_password.html').send(to=[email])

                return Response({"data": "Письмо со сбросом пароля успешно отправлено!", "token": str(refresh.access_token)}, status=status.HTTP_200_OK)
    except:
        return Response({"data": "Данный аккаунт не зарегистрирован или не имеет почтового ящика"}, status=status.HTTP_404_NOT_FOUND)
        

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

            return Response({"data": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)