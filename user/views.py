from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

from shop.models import Product
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from shop.models import Category



def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")

        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)

        user.is_active = True
        user.save()
        messages.success(request, "Tebrikler Giriş Yaptınız")
        subject = "!!!Üye!!!"
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, "tercuman4848@gmail.com"]
        signup_message = "!!!!Müşteri Üyeliği!!!"
        #send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message,fail_silently=False)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')


        return redirect("index")
    context = {
        "form": form,
    }
    return render(request,"register.html", context)


def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.success(request, "Email veya Kullanıcı İsminiz Hatalı.")
            return render(request, "login.html", context)


        login(request, user)
        messages.success(request, "Tebrikler Giriş Yaptınız")
        return redirect("index")
    return render(request,"login.html", context)


def logoutUser(request):
    logout(request)

    return redirect("index")






