from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from customer.forms import RegisterForm


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