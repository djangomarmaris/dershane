from django.shortcuts import render, redirect
from .models import OrderItem,ReturnData,WebhookData
from orders.models import UserTokenData
from .forms import OrderCreateForm
from cart.cart import Cart

from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from shop.models import Category, Product
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import time


# iyzico modülü -> pip install iyzipay
import iyzipay

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.db.models import Q

# Bu verileri, admin panelinden eklenebilir yapacağız

api_key = 'sandbox-etkBOaBAec7Zh6jLDL59Gng0xJV2o1tV'
secret_key = 'sandbox-uC9ysXfBn2syo7ZMOW2ywhYoc9z9hTHh'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
    }

#sozlukToken = list()

sepetClock = list()








@login_required(login_url="user:login")
def order_create(request):
    cart = Cart(request)
    for c in cart:
        print(c)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author=request.user
            order.save()



            for item in cart:
                 newItem = OrderItem.objects.create(order=order,author=request.user,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         )
                 #newItem.product.stock = newItem.product.stock - item['quantity']
                 newItem.product.save()
            # clear the cart
            #cart.clear()
            #return payment(request)
            return redirect('/order/take')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form,
                                                        })

@login_required(login_url="user:login")
def take(request):

    cart = Cart(request)
    """
    jet = Category.objects.filter(name__contains='jet')
    fly = Category.objects.filter(name__contains='fly')
    tur = Category.objects.filter(name__contains='turlar')
    adre = Category.objects.filter(name__contains='adrenalin')
    korsan = Category.objects.filter(name__contains='tekne')
    """
    #show = OrderItem.objects.filter(Q(author=request.user) and Q(paid=False)).order_by('-id')

    #a = OrderItem.objects.all()
    #total = int()
    #for i in a:
        #print(i.order)
        #print(i.price)
        #total += float(i.price)

    #print(total)


    context = {
        #"show": show,
        "cart" : cart
    }
    #'jet':jet,'fly':fly,'tur':tur,'adre':adre,'korsan':korsan, 'success': 'Ödeme Alındı'
    return render(request,"orders/order/take.html",context)


@login_required(login_url="user:login")
def payment(request):

    ts = time.time()
    sepetClock.append(str(int(ts)))
    print(sepetClock[0])
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        print(form,'***********','Form Burada')
        if form.is_valid():
            order = form.save(commit=False)
            order.author=request.user
            order.save()



            for item in cart:
                 newItem = OrderItem.objects.create(order=order,author=request.user,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         )
                 #newItem.product.stock = newItem.product.stock - item['quantity']
                 newItem.save()
    context = dict()
    """
    total = int()
    for c in cart:
        total += float(c['total_price'])
    print(total)
    """

    a = OrderItem.objects.filter(Q(author_id=request.user.id) and Q(paid=False))
    total = int()
    orderID = list()

    for i in a:
        orderID.append(i.order)
        print(i.price * i.quantity)
        total += float(i.price * i.quantity)

    print(orderID)
    print('********')
    print(str(i.order.tc))
    para = float(cart.get_total_price())

    myrequest = request.user


    buyer={
        'id': str(i.order.id),
        'name': str(i.order.first_name),
        'surname': str(i.order.last_name),
        'gsmNumber': str(i.order.phone),
        'email': str(i.order.email),
        'identityNumber': str(i.order.tc),
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': str(i.order.adress),
        'ip': '85.34.78.112',
        'city': str(i.order.city),
        'country': 'Turkey',
        'zipCode': '34732'
        }

    address={
        'contactName': str(i.order.first_name),
        'city': str(i.order.city),
        'country': 'Turkey',
        'address': str(i.order.adress),
        'zipCode': '34732'
        }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': para,
            },

        ]

    request={
        'locale': 'tr',
        'conversationId': sepetClock[0],
        'price': para,
        'paidPrice': para,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://localhost:8000/order/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
        }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    #print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    print("************************")
    UserTokenData.objects.create(userlast=str(i.order.tc), usertoken=json_content["token"])
    json_content["token"]
    # BURADA TOKEN BİLGİSİNİ ORDERITEM 'a YAZIYORUM,
    # RESULT İÇERİSİNDE ÖDEME BAŞARILI OLURSA, PAID -> True OLACAK
    idOrder = OrderItem.objects.filter(order_id=orderID[-1]).update(tokenCheck=str(json_content["token"]))

    return HttpResponse(json_content["checkoutFormContent"])


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    cart = Cart(request)
    a = OrderItem.objects.filter(Q(author_id=request.user.id) and Q(paid=False))
    total = int()
    orderID = list()
    for i in a:
        orderID.append(i.order)
        print(i.price * i.quantity)
        total += float(i.price * i.quantity)
    print(orderID)
    kim = UserTokenData.objects.filter(userlast=str(i.order.tc)).order_by('id')
    son = kim.last()
    print('SON DENEME',son.usertoken)

    context = dict()
    mesaj = request
    url = request.META.get('')
    request = {
        'locale': 'tr',
        'conversationId': sepetClock[0],
        'token': son.usertoken,
        }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    #print(sozlukToken[0])   # Form oluşturulduğunda
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)

    print(sonuc[0][1])
    print(sonuc[2][1])
    print(sonuc[3][1])
    print(sonuc[4][1])
    print(sonuc[5][1])
    print(sonuc[7][1])
    print(sonuc[13][1])
    print(sonuc[20][1])
    print(sonuc[22][1])
    #print(sozlukToken[0])
    print("************************")
    #print(sozlukToken)
    print("************************")
    time.sleep(10)
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        #idOrder = OrderItem.objects.filter(tokenCheck=str(sozlukToken[0])).update(paid=True)


        iyzicoData = ReturnData.objects.create(status=sonuc[0][1],systemtime=sonuc[2][1],conversationİd=sonuc[3][1],price=sonuc[4][1],
                                               paidPrice=sonuc[5][1],
                                               paymentid=sonuc[7][1],
                                               binNumber=sonuc[13][1],
                                               result_token=sonuc[21][1],
                                               payment_token=son.usertoken)
        iyzicoData.save()


        #info = 'Çok Teşekkür Ederim Bizimle Beraber Olman Bizim İçin Çok Önemli Derslerde Görüşmek Üzere...'
        #name = idOrder.order.first_name
        #last = idOrder.order.last_name
        #linkNow = idOrder.product.description
        #email = idOrder.order.email
        #subject = 'Ödemeniz Alınmıştır'
        #from_email = settings.EMAIL_HOST_USER
        #to_email = [from_email, email]
        #contact_message = "WWW.ZEYNEBURAS.COM\n %s\n\İsim: %s\nSoyisim: %s\nLinkler:\n %s" % (
        #info,
        #name,
        #last,
        #linkNow,
        #)
        #send_mail(subject, contact_message, from_email, to_email,fail_silently=True)


        cart.clear()
        messages.success(mesaj,'Teşekkürler,Zoom Derslerin Email Adresine İletildi. ')
        return HttpResponseRedirect(reverse('orders:success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('orders:failure'), context)

    return HttpResponse(url)



def success(request):
    context = dict()
    cart = Cart(request)
    context['cart'] = cart
    context['success'] = 'İşlem Başarılı'
    context['show'] = OrderItem.objects.filter(Q(author=request.user) & Q(paid=True)).order_by('-id')
    template = 'orders/order/ok.html'
    return render(request, template, context)


def fail(request):
    context = dict()
    context['fail'] = 'Ödeme Alınamıştır Lütfen Tekrar Deneyiniz.'

    template = 'orders/order/fail.html'
    return render(request, template, context)





@require_POST
@csrf_exempt
def webhook(request):
    cart = Cart(request)
    jsn = request.body
    my_json = jsn.decode('utf8').replace("'", '"')

    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    print("data", data['iyziEventTime'])
    print("data", data['iyziEventType'])
    print("data", data['iyziReferenceCode'])
    print("data", data['merchantId'])
    print("data", data['paymentConversationId'])
    print("data", data['status'])
    print("data", data['token'])
    if data['status'] == 'success':
        kim = UserTokenData.objects.filter(userlast=request.user).last()
        idOrder = OrderItem.objects.filter(tokenCheck=str(kim.usertoken)).update(paid=True)





        cart.clear()
        messages.success(request,'Teşekkürler,Zoom Derslerin Email Adresine İletildi. ')


    elif data['status'] == 'failure':
        pass


    iyzicowebhook = WebhookData.objects.create(paymentConversation=data['paymentConversationId'],merchant=data['merchantId'],
                                               webhooktoken=data['token'],
                                               status=data['status'],
                                               iyziReferenceCode=data['iyziReferenceCode'],
                                               iyziEventType=data['iyziEventType'],
                                               iyziEventTime=data['iyziEventTime'])
    iyzicowebhook.save()



    return HttpResponse(status=200)