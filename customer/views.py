from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from customer.forms import RegisterForm, LoginForm, CheckoutForm
from adminpanel.models import Product
from customer.models import CusetomerCart, Checkout, CustomerPayedProduct
import razorpay

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
                register_form = RegisterForm(request.POST)
                context = {
                    'form': register_form,
                    'error': 'Username alredy exist add new one'
                }
                return render(request, 'customer/customer_register.html', context)
            elif User.objects.filter(email=email).exists():
                register_form(request.POST)
                context = {
                    'form': register_form,
                    'error': 'email alredy exist add new one'
                }
                return render(request, 'customer/customer_register.html', context)
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

@login_required(login_url = reverse_lazy('login-customer'))
def view_cart(request):
    cart = CusetomerCart.objects.filter(customer=request.user).select_related('product')
    total_price = sum(item.product.price for item in cart)
    checkout_form = CheckoutForm()
    context = {
        'cart': cart,
        'total_price': total_price,
        'form': checkout_form
    }
    return render(request, 'customer/customer_cart.html', context)

@login_required(login_url = reverse_lazy('login-customr'))
def remove_cart_product(request, cart_item_id):
    user = request.user
    cart_object = CusetomerCart.objects.get(customer=user, id=cart_item_id)
    cart_object.delete()
    return redirect(reverse('view-cart'))    

# checkout and payment gateway 
@login_required(login_url = reverse_lazy('login-customer'))
def checkout_customer(request):
    if request.method == 'POST':
        user = request.user
        address = request.POST['address']
        phone = request.POST['phone']
        cart = CusetomerCart.objects.filter(customer=user).select_related('product')
        total_price = sum(item.product.price for item in cart)
        receipt = str(uuid.uuid(1))
        client = razorpay.Client(auth=("rzp_test_8ByHObWr7wXRoA", "vbj5N0Om11HrxPOCqiHGwBbz"))
        DATA = {
            'amount': total_price * 100,
            'currency': 'INR',
            'receipt': 'Shope receipt',
            'payment_capture': 1,
            'notes': {}
        }
        oreder_details = client.order.create(data=DATA)

        checkout_order_instance = Checkout(
            customer = user,
            order_id = oreder_details.get('id'),
            total_amount = total_price,
            reciept_num = receipt,
            delivery_address = address,
            delivery_phoone = phone
        )
        checkout_order_instance.save()
        checkout = Checkout.objects,get(id=checkout_order_instance.id)

        for item in cart:
            orderproduct_instance = CustomerPayedProduct(
                customer = user,
                product_name = item.product.product_name,
                price = item.product.price,
                product_description = item.product.product_discription,
                checkout_details = checkout
            )
            orderproduct_instance.save()
        context = {
            'order_id': oreder_details.get('id'),
            'amount': total_price,
            'amountscript': total_price * 100,
            'currency': 'INR',
            'companyname': 'EcomShope',
            'username': request.user.first_name + ' ' + request.user.last_name,
            'usermail': request.user.email,
            'phonenum': phone,
            'rzpkey': "rzp_test_8ByHObWr7wXRoA",
        }
        return render(request, 'customer/checkout.html', context)
    else:
        return redirect(reverse('products'))

@csrf_exempt
@login_required(login_url = reverse_lazy('login-customer'))
def mark_payment_success(request):
    if request.is_ajax():
        order_id = request.POST['order_id']
        payment_id = request.POST['payment_id']
        payment_singnature = request.POST['payment_signature']
        user = request.user

        cart_order_instance = Checkout.objects.get(order_id=order_id, customer=user)
        cart_order_instance.payment_singnature = payment_singnature
        cart_order_instance.payment_id = payment_id
        cart_order_instance.payment_completed = True
        cart_order_instance.save()
        cart_instance = CusetomerCart.objects.filter(customer=user)
        cart_instance.delete()
        return JsonResponse({'result': 'success'})
        


