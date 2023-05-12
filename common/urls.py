from django.urls import path

from .import views

app_name='common'

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('shop',views.shop,name='shop'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('cart',views.cart,name='cart'),

    path('changepassword',views.change_password,name='change_password'),
    path('product/<int:pid>',views.product_detailes,name='product_detailes'),
    path('logout',views.logout,name='logout'),
    path('order_details',views.order_details,name='order_details'),
    path('payment',views.payment,name='payment'),

    path('mycart/remove/<int:c_id>',views.removecart,name='remove_cart'),
    path('change_qty',views.change_qty,name="change_qty"),
    path("order_payment", views.order_payment, name="orderpayment"),
    path("updatepayment", views.updatepayment, name="updatepayment"),
    path("profile", views.profile, name="profile"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("my_orders", views.my_orders, name="my_orders"),
    path("my_orders/cancel_order/<int:o_id>", views.cancel_order, name="cancel_order"),
    path("search_product", views.search_product, name="search_product"),
]


