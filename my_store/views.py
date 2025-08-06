import re
from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart


# Create your views here.
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        # Query the product database
        searched = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched)
        )
        # Test for Null
        if not searched:
            messages.success(request, "That Product Does Not Exist..Please Try Again")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {"searched": searched})

    else:
        return render(request, "search.html", {})


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did the fill the form
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            # IS THE FORM VALID
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password has been Update...")
                # login(request, current_user)
                return redirect("update_password")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect("update_password")

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form": form})
    else:
        messages.success(request, "You Must be logged In To view that Page..")
        return redirect("home")


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!..")
            return redirect("home")
        return render(request, "Update_user.html", {"user_form": user_form})
    else:
        messages.success(request, "You Must be logged In to access the page..")
        return redirect("home")

    # return render (request, 'update_user.html', {})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, "category_summary.html", {"categories": categories})


def category(request, foo):
    # Replace hyphen with space for friendlier lookup
    foo = foo.replace("-", " ")

    try:
        # Case-insensitive match
        category = Category.objects.get(name__iexact=foo)
        products = Product.objects.filter(category=category)
        return render(
            request, "category.html", {"products": products, "category": category}
        )

    except Category.DoesNotExist:
        messages.warning(request, f"Category '{foo}' does not exist.")
        return redirect("home")


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {"product": product})


def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})


def about(request):
    return render(request, "about.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # convert db string to py dict
            if saved_cart:
                # convert dict to JSON
                converted_cart = json.loads(saved_cart)
                # add the loaded cart dict to our session
                cart = Cart(request)
                # loop thru the cart and add items from the db
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, ("Username Created - Please Fill Out Your User Info Below...")
            )
            return redirect("update_info")
        else:
            messages.success(
                request,
                ("Whoops! There was a problem Registering, please try again..."),
            )
            return redirect("register")
    else:
        return render(request, "register.html", {"form": form})

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
