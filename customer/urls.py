from django.urls import path
from . import views


urlpatterns = [
    path('register-customer', views.register_customer, name='register-customer'),
]