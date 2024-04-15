from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Store_app.models import *

@login_required(login_url="/login")
def home(request):
    return render(request,'dashboard_home.html')

#  -------------------------- Category Section --------------------------------------------

def show_category(request):
    categories = Category.objects.all()
    context=  {
   'categories':categories
   }
    return render(request,'show_category.html',context)


def add_category(request):
    if request.method == "POST":
       name = request.POST['name']
       discount = request.POST['discount']
       image= request.POST['image']
       category = Category(name=name,discount=discount,image=image)
       category.save()
       return redirect("/dashboard/show_category")
    else:

        return render(request,'add_category.html')



def update_category(request,pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
       name = request.POST['name']
       discount = request.POST['discount']
       image= request.POST['image']

       category.name = name
       category.discount = discount
       category.image = image
       category.save()
       return redirect("/dashboard/show_category")
    else:
        return render(request,'update_category.html',{'category':category,})


def delete_category(request,pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect("/dashboard/show_category")


#  -------------------------- Product Section -----------------------------------------

def show_product(request):
    products = Product.objects.all()
    context ={
        'products':products,
    }
    return render(request,'show_product.html',context) 


def add_product(request):
    if request.method == "POST":
       name = request.POST['name']
       category = request.POST['category']
       cat = Category.objects.get(name__exact=category)
    #    print(cat)
       image= request.POST['image']
       digital= request.POST['digital']
       days_to_deliver= request.POST['days_to_deliver']
       price= request.POST['price']
       description= request.POST['description']

       product = Product(name = name,category = cat, image=image,digital=digital,days_to_deliver=days_to_deliver,price=price,description=description)
       product.save()
       return redirect("/dashboard/show_product")
    else:
        return render(request,'add_product.html')



def update_product(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
       name = request.POST['name']
       category = request.POST['category']
       cat = Category.objects.get(name__exact=category)
    #    print(cat)
       image= request.POST['image']
       digital= request.POST['digital']
       days_to_deliver= request.POST['days_to_deliver']
       price= request.POST['price']
       description= request.POST['description']

       product.name = name
       product.category = cat
       product.name = name
       product.image = image
       product.name = digital
       product.days_to_deliver = days_to_deliver
       product.price = price
       product.description = description
       product.save()
       return redirect("/dashboard/show_product")
    else:
        return render(request,'update_product.html', {'product':product})


def delete_product(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect("/dashboard/show_product")




#  ---------------------------- Customer Section ------------------------------------------

def show_customer(request):
    customers = Customer.objects.all()
    context=  {
   'customers':customers
   }
    return render(request,'show_customer.html',context)


def add_customer(request):
    if request.method == "POST":
       name = request.POST['name']
       email = request.POST['email']
       phone = request.POST['phone']
       address = request.POST['address']

       customer = Customer(name=name,email=email,phone=phone,address=address)
       customer.save()
       return redirect("/dashboard/show_customer")
    else:
        return render(request,'add_customer.html')
       


def update_customer(request,pk):      
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
       name = request.POST['name']
       email = request.POST['email']
       phone = request.POST['phone']
       address = request.POST['address']
       
       customer.name = name
       customer.email = email
       customer.phone = phone
       customer.address = address

       customer.save()
    
       return redirect("/dashboard/show_customer")
    else:
        return render(request,'update_customer.html',{'customer':customer})


def delete_customer(request,pk):    
    customer = Customer.objects.get(id=pk)
    customer.delete()
    return redirect("/dashboard/show_customer")

# -------------------------------------Order ------------------------------------------------

def show_order(request):
    orders = Order.objects.all() 
    return render(request,'show_order.html',{'orders':orders,})



#  -------------------------------- OrderItem Section ---------------------------------------------------------



def show_orderItem(request):
    orderitems = OrderItem.objects.all()
    return render(request,'show_orderItem.html',{'orderitems':orderitems})


#  -------------------------- ShippingAddress Section ---------------------------------------------

def show_address(request):
    ship_addresses = ShippingAddress.objects.all()
    return render(request,'show_address.html',{'ship_addresses':ship_addresses})