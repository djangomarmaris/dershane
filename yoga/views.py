from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,reverse,redirect

# Create your views here.
from cart.cart import Cart
from shop.models import Category

from django.conf import settings
from django.core.mail import send_mail

from yoga.models import kvvk ,Documents ,Exam

from .forms import UploadFileForm



def index(request):
    pdf = kvvk.objects.all()
    online = Category.objects.filter(name__contains='online')
    cart = Cart(request)
    print(request.user)
    context = {
        'cart':cart,
        'online':online,
        'pdf':pdf
    }
    return render(request,'central/index.html',context)




def about(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }
    return render(request,'central/about.html',context)


def mentor(request):
    cart = Cart(request)
    if 'btnSubmit' in request.POST:
        if True:
            hotel= 'Turban/İletişim Formu'
            name = request.POST.get('name')
            email = request.POST.get('email')
            info = request.POST.get('info')

            subject = 'Costumer Contact Messages'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email,"djangomarmaris@gmail.com"]
            contact_message = "Name:%s\nEmail:%s\nHotel:%s\nInfo:%s" % (
                name,
                email,
            hotel,
            info)
            send_mail(subject, contact_message, from_email, to_email, fail_silently=True)
        return redirect('/')

    context = {
        'cart': cart
    }
    return render(request,'central/mentor.html',context)

def share(request):
    cart = Cart(request)
    if 'btnSubmit' in request.POST:
        if True:
            name = request.POST.get('name')
            email = request.POST.get('email')
            info = request.POST.get('info')

            subject = 'Costumer Contact Messages'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email,"djangomarmaris@gmail.com"]
            contact_message = "Name:%s\nEmail:%s\nInfo:%s" % (
                name,
                email,
            info)
            send_mail(subject, contact_message, from_email, to_email, fail_silently=True)
        return redirect('/')
    context = {
        'cart': cart
    }
    return render(request,'central/share.html',context)

def question(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }
    return render(request,'central/question.html',context)



def yoga(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }
    return render(request,'central/yoga.html',context)


def contact(request):
    if 'btnSubmit' in request.POST:
        if True:
            name = request.POST.get('name')
            email = request.POST.get('email')
            info = request.POST.get('info')

            subject = 'Costumer Contact Messages'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email,"djangomarmaris@gmail.com"]
            contact_message = "Name:%s\nEmail:%s\nInfo:%s" % (
                name,
                email,
            info)
            send_mail(subject, contact_message, from_email, to_email, fail_silently=True)
        return redirect('/')


    return render(request,'central/contact.html')



def document(request):
    products = Documents.objects.all().order_by('-id')



    context = {

        'products':products
    }
    return render(request,'central/document.html',context)


@login_required(login_url="user:login")
def upload(request):
    name = request.POST.get('name')
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            student = Exam.objects.create(name=name,paper=file)
            student.save()
    else:
        form =UploadFileForm()
    return render(request,'central/upload.html',{'form':form})