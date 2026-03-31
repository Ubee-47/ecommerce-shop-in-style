from django.shortcuts import render,redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms  import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payments.forms import ShippingForm # type: ignore
from payments.models import ShippingAddress # type: ignore
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart





# Create your views here.
# home page
def home(request):
    products = Product.objects.all()
    return render(request,'home.html', {'products': products})

# about page
def about(request):
     return render(request,'about.html', {})


# login user
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
           # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
            saved_cart = current_user.old_cart
			# Convert database string to python dictionary
            if saved_cart:
				# Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
                cart = Cart(request)
				# Loop thru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request,("you have been logged in!"))
            return redirect('home')
        else:
            messages.success(request,("There was an error, Please try again..."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

# search
def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	
	


# logout
def logout_user(request):
    logout(request)
    messages.success(request,("you have been logged out ..."))
    return redirect('home')


# update profile...
def update_user(request):
        if request.user.is_authenticated:
            current_user = User.objects.get(id=request.user.id)
            user_form = UpdateUserForm(request.POST or None, instance = current_user)
            
            if user_form.is_valid():
                user_form.save()

                login(request, current_user)
                messages.success(request, "User Has Been Upadated!! ")
                return redirect('home')
            return render(request, 'update_user.html', {'user_form':user_form})
        else:
            messages.success(request, "You must be logged in to  access that page !! ")
            return redirect('home')

# update user info

def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')





# update password
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #  did you fill up the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # is valid or not 
            if form.is_valid():

                form.save()
                messages.success(request, "Your password has been Update, Please login again!!!")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html' ,{'form':form})    
    else:
        messages.success(request, "You must be logged in to  view  that page !! ")
        return redirect('home')

    

	  

# regester form 
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password = password)
            login(request, user)
            messages.success(request,("Username is create  successfuly, Please fill out your info Below ..."))
            return redirect('update_info')
        else:
            messages.success(request,("Whoops! there is a problem Registering, Please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})





# product page
def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})

# # category page
# def category(request,foo):
#     # Replace hyphen with spaces
#     foo = foo.replace('-', ' ')
#     # grab the category from urls   
#     # category = Category.objects.get(name=foo)
#     category = get_object_or_404(Category, name=foo)
#     products = Product.objects.filter(category=category)
#         # print(category)
#     return render(request, "category.html", {'products':products, 'category':category}) 
    
# category
def category(request, foo):
    # replace hyphens with spaces
    foo = foo.replace('-', ' ')
    # Grab category from url
    category = Category.objects.get(name=foo)
    products = Product.objects.filter(category=category)
       
    # context={
    #     'category':category,
    #     'products':products,
    #     }
       
    # return render(request, 'category.html', context)
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
       
        context={
        'category':category,
        'products':products
        }
       
        return render(request, 'category.html', context)
    except:
        messages.success(request, (" This Category does not exist"))
        return redirect('home')    

# category Summary
def category_summary(request):
    categories =Category.objects.all()
    return render(request,'category_summary.html', {'categories':categories})
