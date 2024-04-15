
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='admin page'),

    # ------------------- Category section --------------------------------
    path('show_category', views.show_category, name='show_category'),
    path('add_category', views.add_category, name='add_category'),
    path('update_category/<int:pk>', views.update_category, name='update_category'),
    path('delete_category/<int:pk>', views.delete_category, name='delete_category'),
    
    # -------------------- Product Section --------------------------------------
    path('show_product', views.show_product, name='show_product'),
    path('add_product', views.add_product, name='add_product'),
    path('update_product/<int:pk>', views.update_product, name='update_product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),

    # --------------------- Customer Section --------------------------------------
    path('show_customer', views.show_customer, name='show_customer'),
    path('add_customer', views.add_customer, name='add_customer'),
    path('update_customer/<int:pk>', views.update_customer, name='update_customer'),
    path('delete_customer/<int:pk>', views.delete_customer, name='delete_customer'),

    # ---------------------- Order Section -----------------------------------------
    path('show_order', views.show_order, name='show_order'),

    # ---------------------  OrderItem  Section---------------------------------------
    path('show_orderItem', views.show_orderItem, name='show_orderItem'),

    # ------------------- Shipping Address Section ------------------------------------
    path('show_address', views.show_address, name='show_address'),




]   




#  Developed By Naresh Kumar Agrawal