from django.urls import path
from .views import (
    RegistrationAPIView,
    ClientAdminRegistrationAPIView,
    LoginAPIView,
)


app_name = 'authentication'

urlpatterns = [
    path('api/v1/register', RegistrationAPIView.as_view(), name='register'),
    path('api/v1/register/company',
         ClientAdminRegistrationAPIView.as_view(), name='register_company'),
    path('api/v1/login', LoginAPIView.as_view(), name='login'),
]