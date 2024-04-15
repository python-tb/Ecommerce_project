from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth,messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories':categories,
        'products':products,
        
    }
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order,created = Order.objects.get_or_create(customer=customer,complete= False)
        my_wishlist = Wishlist.objects.get(customer=customer)
        
        context.update({'order':order,'my_wishlist':my_wishlist,})
    return render(request,'index.html',context)


@login_required(login_url="/login")   # required double quote " " in login url not signle
def cart(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    # print(user, customer, order)
    orderItems = OrderItem.objects.filter(order=order)
    categories = Category.objects.all()
    my_wishlist = Wishlist.objects.get(customer=customer)
    
    context = {
        'order': order,
        'items' : orderItems,
        'categories':categories,
        'my_wishlist':my_wishlist,
    }
    return render(request,'cart.html',context)


@login_required(login_url="/login") 
def checkout(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItems = OrderItem.objects.filter(order=order)
    categories = Category.objects.all()
    my_wishlist = Wishlist.objects.get(customer=customer)
    
    context = {
        'order': order,
        'items' : orderItems,
        'categories':categories,
        'customer':customer,
        'my_wishlist':my_wishlist,
    }
    if request.method == 'POST':
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        payment = request.POST['payment']

        new_address =ShippingAddress.objects.create(address=address,city=city,state=state,country=country,zip_code=zip_code)
        order.mode_of_payment = payment
        order.complete = True
        order.save()
        new_address.save()

    return render(request,'checkout.html',context)


def contact(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request,'contact.html',context)



def detail(request,pk):
    product = Product.objects.get(id=pk)
    products = Product.objects.all()
    categories = Category.objects.all()
   
    context = {
        'product':product,
        'products':products,
        'categories':categories,
          
     }
    return render(request,'detail.html',context)



#  ------------------------------------  Search Bar & Pagination Functionality -------------------------------



def shop(request,category=None):
    categories = Category.objects.all()    
    context = {}
    if request.method == "POST":
        search_text = request.POST['product']
        products = Product.objects.filter(name__contains=search_text)  # contains Use for searching a short name
    else:
        if category == 'all':
            products = Product.objects.all()
            paginator = Paginator(products,3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            total_page = page_obj.paginator.num_pages
            context.update({'category_name': 'All Products', 
                              'page_obj':page_obj,
                              'totalpageList':[n+1 for n in range(total_page)]})    # 'All Products' | we pass a string
        else:
            products = Product.objects.filter(category=category)
            category = Category.objects.get(id=category)
            context.update({'category_name': category.name})

        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            order,created = Order.objects.get_or_create(customer=customer,complete= False)
            my_wishlist = Wishlist.objects.get(customer=customer)
            
            context.update({'order':order,'my_wishlist':my_wishlist,})

    context.update({
        'products':products,
        'categories':categories,

     })
    return render(request,'shop.html',context)


# ------------------------- Add To Cart Functionality  --------------------------------------------------------


@login_required(login_url="/login")
def addToCart(request,pk):
    user = request.user
    customer = Customer.objects.get(user=user)
    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    product = Product.objects.get(id=pk)

    try:
        order_item = OrderItem.objects.get(product=product, order=order)
        order_item.quantity+=1
        order_item.save()
    except:
        order_item = OrderItem.objects.create(product=product, order=order, quantity =1)
        order_item.save()
    return redirect("/cart")


def quantityup(request,pk):
    user = request.user
    customer = Customer.objects.get(user=user)
    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item = OrderItem.objects.get(id=pk)
    order_item.quantity += 1
    order_item.save()
    return redirect("/cart")

def quantitydown(request,pk):
    user = request.user
    customer = Customer.objects.get(user=user)
    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item = OrderItem.objects.get(id=pk)
    if order_item.quantity <= 1:       #  | here logic for less than 1 qty. auto delete.. 
        order_item.delete()
        order.save()
    else:
        order_item.quantity -= 1
        order_item.save()
        order.save()
    return redirect("/cart")


def removeproduct(request,pk):
    user = request.user
    customer = Customer.objects.get(user=user)
    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item = OrderItem.objects.get(id=pk)
    order_item.delete()
    order.save()
    return redirect("/cart")




def sorted_products(request,type):
    categories = Category.objects.all()
    context = {}

# l2h means Ascending order means low2high or h2l means descending order means high2low..

    if type == "l2h":
        products = Product.objects.all().order_by('price')
    else:
        products = Product.objects.all().order_by('-price')
    context = ({
        'products':products,
        'categories':categories, })
    if request.user.is_authenticated:
        customer = Customer.objects.get(user = request.user)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        context.update({'order':order,})

    return render(request,'shop.html',context)



# ---------------------- Add To WishList Section ----------------------------------------------------------------



def view_wishlist(request):
    user = request.user
    customer = Customer.objects.get(user=request.user)
    wishlist = Wishlist.objects.filter(customer=customer).first()
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
   
    categories = Category.objects.all()
    context={
        'wishlist_items':wishlist_items,
        'categories':categories,
        
    }
    return render(request,'view_wishlist.html',context)


def add_wishlist(request,pk):
    product = get_object_or_404(Product,id=pk)
    user = request.user
    customer = Customer.objects.get(user=request.user)
    wishlist,created = Wishlist.objects.get_or_create(customer=customer)
    WishlistItem.objects.create(wishlist=wishlist,product=product)
    return redirect('/view_wishlist')


def remove_wishlist(request,pk):
    item = get_object_or_404(WishlistItem, id=pk)
    item.delete()
    return redirect('/view_wishlist')







   



# --------------------------------------------Authentication and Authorization------------------------------ 



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info("Please Enter Correct username and Password")
            return redirect("/login")
    else:

        return render(request,'login.html')



def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email = email).exists():
            messages.info(request,"Email Already exists")
            return redirect("/signup")

        if User.objects.filter(username = username).exists():
            messages.info(request,"Username Already exists")
            return redirect("/signup")

        new_user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
        new_user.save()

        return redirect("/login")
    else:
        return render(request,'signup.html')
    

def logout(request):
   auth.logout(request)
   return redirect("/login")


