from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from adminpanel.forms import LoginForm, ProductForm
from adminpanel.models import Product


@login_required(login_url=reverse_lazy('login'))
def admin_dashboard(request):
    return render(request, 'adminpanel/admin_dashboard.html')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('admindashboard'))
    else:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active and user.is_superuser:
                        login(request,user)
                        return redirect(reverse('admindashboard'))
                    else:
                        return HttpResponse('Your account is not active')
                else:
                    return HttpResponse('The Account does not exixts')
            else:
                login_form = LoginForm(request.POST)
                return render(request, "adminpanel/admin_login.html", {"form": login_form})
        else:
            login_form = LoginForm()
        return render(request, "adminpanel/admin_login.html", {"form": login_form})

def checksuperuser(user):
    return user.is_superuser

@user_passes_test(checksuperuser, login_url= reverse_lazy('login'))
def admin_logout(request):
    logout(request)
    return redirect(reverse('login'))

@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def manage_products(request):
    product = Product.objects.all()
    context = {'products': product}
    return render(request, 'adminpanel/manage_product.html', context)

@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def add_products(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            
            product_object = Product()
            product_object.product_name = product_form.cleaned_data['product_name']
            product_object.product_discription = product_form.cleaned_data['product_discription']
            product_object.price = product_form.cleaned_data['price']
            product_object.product_picture = request.FILES['product_image']
            product_object.save()
            return redirect(reverse('manage-products'))
        else:
            product_form = ProductForm(request.POST, request.FILES)
            return render(request, 'adminpanel/add_product.html', {'form': product_form})
    else:
        product_form = ProductForm()
        return render(request, 'adminpanel/add_product.html', {'form': product_form})


@csrf_exempt
@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def chage_status(request):
    if request.is_ajax():
        product_id = int(request.POST['product'])
        action = request.POST['action']
        product_object = Product.objects.get(id=product_id)
        if action == 'disabled':
            product_object.is_active = False
        else:
            product_object.is_active = True

        product_object.save()
        return JsonResponse({'result': 'success'})




