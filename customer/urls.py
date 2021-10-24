from django.urls import path
from . import views


urlpatterns = [
    path('products', views.home, name='products'),
    path('register-customer', views.register_customer, name='register-customer'),
    path('login-customer', views.login_customer, name='login-customer'),
    path('logout-customer', views.logout_customer, name='logout-customer'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart', views.remove_from_cart, name='remove-from-cart'),
    path('view-cart', views.view_cart, name='view-cart'),
    path('remove-cart-product', views.remove_cart_product, name='remove-cartproduct'),
]