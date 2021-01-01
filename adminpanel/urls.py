from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('login', views.admin_login, name="login"),
    path('', RedirectView.as_view(url='login')),
    path('admin-logout', views.admin_logout, name="adminlogout"),
    path('dashboard', views.admin_dashboard, name="admindashboard"),
    path('manage-products', views.manage_products, name="manage-products"),
    path('add-products', views.add_products, name="add-products"),
    path('change-status', views.chage_status, name="change-status"),
    path('edit-product/<int:product_id>', views.edit_products, name="edit-products"),
    path('delete-product/<int:product_id', views.delete_product, name="delete-product"),
]