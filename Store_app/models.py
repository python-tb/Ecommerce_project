
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=70)
    discount = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        url = ""
        try:
            url = self.image.url
        except:
            url = ""
        return url

    @property
    def cat_count(self):
        products = self.product_set.all()
        num = products.count()
        return num


class Order(models.Model):
    customer = models.ForeignKey(
    Customer, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    mode_of_payment = models.CharField(max_length=50)
    status = models.CharField(max_length=40)

    def __str__(self):
        return self.customer.name + " " + str(self.id)

    @property
    def getCartTotal(self):
        items = self.orderitem_set.all()
        totalPrice = sum(item.getItemTotal for item in items)
        return totalPrice

    @property
    def getTotalItems(self):
        items = self.orderitem_set.all()
        totalNumber = sum(item.quantity for item in items)
        return totalNumber


class Product(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField()
    days_to_deliver = models.IntegerField()
    price = models.IntegerField(default=0)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        url = ""
        try:
            url = self.image.url
        except:
            url = ""
        return url


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.order.customer.name + " - Order-" + str(self.order.id) + " - " + self.product.name + " (" + str(self.quantity) + ")"

    @property
    def getItemTotal(self):
        return self.quantity*self.product.price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=60)
    zip_code = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.address + " - "+self.order.customer.name



class Wishlist(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "Wishlist-" + str(self.id) + self.customer.name

    
    @property
    def getWishListTotal(self):
        items = self.wishlistitem_set.all().count()
        return items




class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.wishlist.customer.name + "- Wishlist | Product-" + self.product.name







