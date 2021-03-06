import datetime
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from adminpanel.forms import LoginForm, ProductForm
from adminpanel.models import Product
from customer.models import CustomerPayedProduct, Checkout



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

# managing products details
@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def manage_products(request):
    product = Product.objects.all()
    context = {'products': product}
    return render(request, 'adminpanel/manage_product.html', context)

@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def add_products(request):
    title = 'Add'
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
    return render(request, 'adminpanel/add_product.html', {'form': product_form, 'title': title})


@csrf_exempt
@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def chage_status(request):
    if request.is_ajax():
        product_id = int(request.POST['product'])
        action = request.POST['action']
        product_object = Product.objects.get(id=product_id)
        if action == 'disable':
            product_object.is_active = False
        else:
            product_object.is_active = True

        product_object.save()
        return JsonResponse({'result': 'success'})


@user_passes_test(checksuperuser, login_url=reverse_lazy('login'))
def edit_products(request, product_id):
    title = 'Edit'
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            
            product_object = Product.objects.get(id=product_id)
            product_object.product_name = product_form.cleaned_data['product_name']
            product_object.product_discription = product_form.cleaned_data['product_discription']
            product_object.price = product_form.cleaned_data['price']
            if request.FILES:
                product_object.product_picture = request.FILES['product_image']
            product_object.save()
            return redirect(reverse('manage-products'))
        else:
            product_form = ProductForm(request.POST, request.FILES)
            return render(request, 'adminpanel/add_product.html', {'form': product_form})
    else:
        product_object = Product.objects.get(id=product_id)
        product_form = ProductForm(initial={
            'product_name': product_object.product_name,
            'product_discription': product_object.product_discription,
            'price': product_object.price,
            'product_image': product_object.product_picture
        })
    return render(request, 'adminpanel/add_product.html', {'form': product_form, 'title': title, 'current_image': product_object.product_picture})


@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect(reverse('manage-products'))


# managing user details
@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def manage_user(request):
    users = User.objects.filter(is_superuser=False, is_staff=False)
    return render(request, 'adminpanel/manage_user.html', {'users': users})

@csrf_exempt
@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def change_user_status(request):
    if request.is_ajax():
        action = request.POST['action']
        user_id = request.POST['user_id']
        user = User.objects.get(id=user_id)
        if action == 'disable':
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return JsonResponse({'result': 'success'})

@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect(reverse('manage-users'))

@user_passes_test(checksuperuser, login_url = reverse_lazy('login'))
def user_details(request, user_id):
    user = User.objects.get(id=user_id)
    orders = CustomerPayedProduct.objects.filter(customer=user_id, checkout_details__payment_completed=True)
    context = {
        'user': user,
        'orders': orders
    }
    return render(request, 'adminpanel/user_view.html', context)

@user_passes_test(checksuperuser, login_url=reverse_lazy('login'))
def view_reports(request):
    return render(request, 'adminpannel/admin_reports.html')

@user_passes_test(checksuperuser, login_url=reverse_lazy('login'))
def daily_sales_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename="salesreport"' + str(datetime.date.today()) + '".csv'
    writer = csv.writer(response)
    tody_min = datetime.datetime.combine(datetime.data.today(), datetime.min)
    tody_max = datatime.datetime.combine(datetime.date.today(), datatime.time.max)
    sales = Checkout.objects.filter(payedon__range=(tody_min, tody_max))
    writer.writerow(['Order_id', 'Payment_id', 'Ammount', 'Reciept', 'Phone no', 'Address'])
    for sale in sales:
        writer.writerow([
            sale.order_id, sale.payment_id, sale.total_amount, sale.reciept_num, sale.delivery_phone, sale.delivery_address
            ])
    return response
