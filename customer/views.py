from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from customer.forms import RegisterForm, LoginForm
from adminpanel.models import Product
from customer.models import CusetomerCart


def home(request):
    products = Product.objects.filter(is_active=True)
    usercart = []
    if request.user.is_authenticated:
        usercart = CusetomerCart.project.filter(customer = request.user)
    context = {
        'products': Products,
        'cart': usercart
    }
    return render(request, 'customer/products.html', context)


def register_customer(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            first_name = register_form.cleaned_data['firstname']
            last_name = register_form.cleaned_data['lastname']
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                register_form(request.POST)
                context = {
                    'form': register_form,
                    'error': 'Username alredy exist add new one'
                }
                return render(request, 'customer/custemer_register.html', context)
            elif User.objects.filter(email=email).exists():
                register_form(request.POST)
                context = {
                    'form': register_form,
                    'error': 'email alredy exist add new one'
                }
                return render(request, 'customer/custemer_register.html', context)
            else:
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password
                )
                user.save()

                return redirect(reverse('login-customer'))
        else:
            register_form = RegisterForm(request.POST)
            context = { 'form': register_form }
            return render(request, 'customer/customer_register.html', context)
    else:
        register_form = RegisterForm()
        context = { 'form': register_form }
        return render(request, 'customer/customer_register.html', context)

def login_customer(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('products'))
                else:
                    login_form = LoginForm(request.POST)
                    context = {
                        'form': login_form,
                        'error': 'This account is not active'
                        }
                    return render(request, 'customer/customer_login.html', context)
            else:
                login_form = LoginForm(request.POST)
                context = {
                    'form': login_form,
                    'error': 'incorrect username or password'
                    }
                return render(request, 'customer/customer_login.html', context)  
        else:
            login_form = LoginForm(request.POST)
            context = { 'form': login_form }
            return render(request, 'customer/customer_login.html', context)  
    else:
        login_form = LoginForm()
        context = { 'form': login_form }
        return render(request, 'customer/customer_login.html', context)  


@login_required(login_url = reverse_lazy('login-customer'))
def logout_customer(request):
    logout(request)
    return redirect(reverse('products'))

@csrf_exempt
@login_required(login_url = reverse_lazy('login-customer'))
def add_to_cart(request):
    if request.is_ajax():
        product_id = int(request.POST['product'])
        user = request.user
        cart_object = CusetomerCart(product = product_id, customer = user)
        cart_object.save()
        return JsonResponse({ 'result': 'product added' })

@csrf_exempt
@login_required(login_url = reverse_lazy('login-customer'))
def remove_from_cart(request):
    if request.is_ajax():
        product_id = int(request.POST['product'])
        user = request.user
        cart_object = CusetomerCart(product = product_id, customer = user)
        cart_object.delete()
        return JsonResponse({ 'result': 'product removed from cart' })


    
