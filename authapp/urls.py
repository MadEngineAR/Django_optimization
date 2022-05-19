from django.contrib import admin
from django.urls import path

from authapp.views import RegisterFormView, Logout, ProfileFormView, LoginFormView

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('profile/', ProfileFormView.as_view(), name='profile'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verification/<str:email>/<str:activate_key>', RegisterFormView.verification, name='verification')]
