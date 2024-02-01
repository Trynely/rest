from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # -------- JWT auth --------
    
    path('token/', views.MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('get-jwt-token-without-password/', views.getJwtTokenWithoutPassword),
    path('api/token/verify/', TokenVerifyView.as_view()),

    path('avatar/<int:pk>/', views.UserAvatar.as_view()),
    path('register/', views.UserRegister.as_view()),
    path('change-password/', views.UserChangePassword.as_view()),

    path('test/', views.Test.as_view()),
    path('test/model/', views.TestModel.as_view()),
    
    # -------- reset password --------
    
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('reset/<str:uidb64>/<str:token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # -------- sessions auth --------

    # path('user/', views.UserView.as_view(), name='user'),
    # path('login/', views.UserLogin.as_view(), name='login'),
    # path('logout/', views.UserLogout.as_view(), name='logout'),
    # path('csrf/', views.csrf),
    # path('ping/', views.ping),

    path('send-reset-password-to-email/', views.sendToEmailResetPassword),
]