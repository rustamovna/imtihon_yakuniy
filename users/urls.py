from django.urls import path
from .views import (
    RegisterView, ProfileView, LoginView,
    PasswordResetRequestView, PasswordResetConfirmView, PasswordResetCompleteView,UserLogoutView
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/',UserLogoutView.as_view(),name='logout')
]
