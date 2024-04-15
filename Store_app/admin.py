from django.contrib import admin
from .models import *

admin.site.register([Customer, Category, Order, Product, OrderItem, ShippingAddress,Wishlist,WishlistItem])
