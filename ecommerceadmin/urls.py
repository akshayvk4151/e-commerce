from django.urls import path

from .import views

app_name='ecommerceadmin'

urlpatterns = [
    path('home',views.index,name='adminhome'),
    path('',views.login,name='login'),
    path('catalogue',views.catalogue,name='catalogue'),
    path('addproduct',views.add_product,name='add_product'),
    path('updatestock',views.update_stock,name='update_stock'),
    path('orderhistory',views.order_history,name='order_history'),
    path('customers',views.customers,name='customers'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('reviews',views.reviews,name='reviews'),
    path('change_password',views.change_password,name='change_password'),


    path('get_product',views.get_product,name='get_product'),
    path('product/delete_product/<int:pid>',views.delete_product,name='delete_product'),









]