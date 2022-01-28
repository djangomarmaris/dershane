from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from  cart.forms import CartAddProductForm
from .models import Category,Product



def Show(request, category_slug = None):
    jet = Category.objects.filter(name__contains='jet')
    fly = Category.objects.filter(name__contains='fly')
    tur = Category.objects.filter(name__contains='turlar')
    adre = Category.objects.filter(name__contains='adrenalin')
    korsan = Category.objects.filter(name__contains='tekne')
    products = Product.objects.filter(available=True).order_by('id')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,'shop/products/show.html',{'category':category,'products':products,'jet':jet,'fly':fly,'tur':tur,'adre':adre,'korsan':korsan})





def product_list(request):
    me = CartAddProductForm()

    jet = Category.objects.filter(name__contains='jet')
    fly = Category.objects.filter(name__contains='fly')
    tur = Category.objects.filter(name__contains='turlar')
    adre = Category.objects.filter(name__contains='adrenalin')
    korsan = Category.objects.filter(name__contains = 'tekne')
    products = Product.objects.filter(available=True).order_by('?')

    return render(request, 'shop/products/list.html',{'products':products,
                                                      'me':me,'jet':jet,'fly':fly,'tur':tur,'adre':adre,'korsan':korsan})




def product_detail(request,id, slug):
    jet = Category.objects.filter(name__contains='jet')
    fly = Category.objects.filter(name__contains='fly')
    tur = Category.objects.filter(name__contains='turlar')
    adre = Category.objects.filter(name__contains='adrenalin')
    korsan = Category.objects.filter(name__contains='tekne')
    product = get_object_or_404(Product, id = id , slug=slug, available=True)
    form = CartAddProductForm()

    article = get_object_or_404(Product,id=id)




    return render(request,'shop/products/detail.html',{'product':product,'form':form ,'jet':jet,'fly':fly,'tur':tur,'adre':adre,'korsan':korsan})





