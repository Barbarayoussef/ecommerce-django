from django.shortcuts import redirect, render
from .models import Product , Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ProductForm
from django import forms
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
from cart.cart import Cart
import json


def edit_product(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product updated successfully!")
                return redirect('product', pk=product.id)
        else:
            form = ProductForm(instance=product)
        return render(request, 'edit_product.html', {'form': form, 'product': product})
    else:
        messages.error(request, "You do not have permission to edit this product.")
        return redirect('home')


def delete_product(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id=pk)
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('home')
    else:
        messages.error(request, "You do not have permission to delete this product.")
        return redirect('home')





def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product added successfully!")
                return redirect('home')
        else:
            form = ProductForm()  # This ensures 'form' is defined for GET requests
        return render(request, 'add_product.html', {'form': form})
    else:
        messages.error(request, "You must be a superuser to access this page.")
        return redirect('home')



def search(request):
    #Determine if they filled out the form
    if request.method == "POST":
        searched= request.POST['searched']
        #Query Products in DB
        searched=Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #test for null
        if not searched:
          messages.success(request,("That product does not exist.. Please try again with different one"))
          return render(request,"search.html",{})
        else:
         return render(request,"search.html",{'searched': searched})
    else:
       return render(request,"search.html",{})
 




def update_info(request):
    if request.user.is_authenticated:
        current_user=Profile.objects.get(user__id=request.user.id)
        shipping_user=ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form=ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request,("YOur Info has Been Updated!!"))
            return redirect('home')
        return render(request,'update_info.html',{'form': form, 'shipping_form':shipping_form})
    else:
        messages.success(request,("You must be logged in to access this page"))
        return redirect('home')
    



def update_password(request):
    if request.user.is_authenticated:
        current_user=request.user
        #did they fill out the form?
        if request.method== 'POST':
            form = ChangePasswordForm(current_user,request.POST)
            # is the form valid
            if form.is_valid():
                form.save()
                messages.success(request,("Your password has been updated"))
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password')
        else:
            form=ChangePasswordForm(current_user)
            return render(request,"update_password.html",{'form': form})
    else:
        messages.success(request,("You must be logged in to access this page"))
        return redirect('home')






def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request,("User has Been Updated!!"))
            return redirect('home')
        return render(request,'update_user.html',{'user_form': user_form})
    else:
        messages.success(request,("You must be logged in to access this page"))
        return redirect('home')




def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',{"categories" : categories}) 


def category(request, foo):
    #Replace Hyphens with Spaces
    foo=foo.replace('-',' ')
    # Grap the category from the url
    try:
        #look up the category
        category= Category.objects.get(name = foo)
        products = Product.objects.filter(Category=category)
        return render(request, 'category.html',{'products': products, 'category': category }) 
    except:
         messages.success(request,("That category does not exist"))
         return redirect('home')
    

def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            #do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #get their saved cart from db
            saved_cart=current_user.old_cart
            #convert db str to python dic
            if saved_cart:
                #convert to dic using JSON
                converted_cart= json.loads(saved_cart)
                #Add the loaded cart dic to the session
                #get the cart
                cart=Cart(request)
                #loop thru the cart and the items from the db
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request,("You have been Logged in"))
            return redirect('home')
        else:
             messages.success(request,("There was an error, try again"))
             return redirect('login')
    else:
        return render(request,'login.html',{})

   

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out.."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            # log in user
            user=authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,("Please Fill out your info below"))
            return redirect('update_info')
        else:
            messages.success(request,("There is a problem, please try again"))
            return redirect('register')
    else:
       return render(request,'register.html',{'form':form})