

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage' ),
    path('cart', views.cart, name='cart' ),
    path('checkout', views.checkout, name='checkout' ),
    path('contact', views.contact, name='contact' ),
    path('detail/<int:pk>', views.detail, name='detail' ),
    path('shop/<str:category>', views.shop, name='shop' ),   # str:category | me str ki  id v integer form m ja rha hota hai
    path('sort/<str:type>',views.sorted_products, name='sorted_products' ),   
    path('add_to_cart/<int:pk>', views.addToCart, name='add_to_cart' ),
    path('view_wishlist', views.view_wishlist, name='view_wishlist'),
    path('add_wishlist/<int:pk>', views.add_wishlist, name='add_to_wishlist' ),
    path('remove_wishlist/<int:pk>', views.remove_wishlist, name='remove_wishlist' ),
    path('quantityup/<int:pk>', views.quantityup, name='quantityup' ),
    path('quantitydown/<int:pk>', views.quantitydown, name='quantitydown' ),
    path('removeproduct/<int:pk>', views.removeproduct, name='removeproduct' ),
    path('login', views.login, name='login' ),
    path('signup', views.signup, name='signup' ),
    path('logout', views.logout, name='logout' ),
]




