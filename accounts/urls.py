from django.urls import path
from accounts.views import *

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('otp/', OTPView.as_view(), name='otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('phone/', ResetPasswordPhoneView.as_view(), name='phone'),
    path('otp_reset/', ResetPasswordOTPView.as_view(), name='otp_reset'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('home/<int:id>', HomeView.as_view(), name="home"),
    path('logout/', UserLogout.as_view(), name="logout"),
]