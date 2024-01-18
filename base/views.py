import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from base.forms import CustomAuthenticationForm, CustomUserCreationForm
from base.models import Category, Product, ProductImages, Order, OrderItem


# Create your views here.

def home(request):
    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()
    category_products = {}
    for category in all_categories:
        products = Product.objects.filter(category=category).order_by('-created')[:3]
        category_products[category] = products
    categories = Category.objects.filter(parent__isnull=True)
    context = {'categories': categories, 'category_products': category_products, 'reg_form': registration_form ,'login_form': login_form}
    return render(request, 'index.html', context)

def category_page(request, cid):
    category = Category.objects.get(id=cid)
    print(category.title)
    if category.parent_id:
        productsz = Product.objects.filter(category=category)

    else:

        child_categories = category.children.all()
        productsz = Product.objects.filter(
            Q(category__in=child_categories) | Q(category=category))

    categoriesnav = []
    categorynav = Category.objects.get(id=cid)

    while categorynav.parent_id:
        categoriesnav.insert(0, categorynav)
        categorynav = Category.objects.get(id=categorynav.parent_id)

    categoriesnav.insert(0, categorynav)  # Insert the last category (the root) after the loop
    print(categoriesnav)

    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()
    category_products = {}
    for categoryz in all_categories:
        products = Product.objects.filter(category=categoryz).order_by('-created')[:3]
        category_products[categoryz] = products
    categories = Category.objects.filter(parent__isnull=True)
    category_products = {}
    context = {'categories': categories, 'category_products': category_products, 'reg_form': registration_form , 'login_form': login_form, 'products': productsz, 'catnav':categoriesnav, 'cat': category }
    return render(request, 'sections.html', context)


def product(request, pid):
    product = Product.objects.get(id=pid)
    if product:
        productimages = ProductImages.objects.filter(product_id=product.id)
    else:
        return HttpResponse(status=404)
    categoriesz = []
    categorynav = Category.objects.get(id=product.category.id)
    categoriesz.insert(0, categorynav)
    while categorynav.parent_id:
        categorynav = Category.objects.get(id=categorynav.parent_id)
        categoriesz.insert(0, categorynav)
    print(categoriesz)
    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()
    category_products = {}
    for category in all_categories:
        products = Product.objects.filter(category=category).order_by('-created')[:3]
        category_products[category] = products
    categories = Category.objects.filter(parent__isnull=True)
    context = {'categories': categories, 'category_products': category_products, 'reg_form': registration_form , 'login_form': login_form, 'images': productimages, 'product': product, 'catnav':categoriesz }
    return render(request, 'product.html', context)


def login_user(request):
    print("processing login")
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponse(status=200)

            else:
                return HttpResponse(status=401)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=500)


def register_user(request):
    if request.method == "POST":
        registration_form = CustomUserCreationForm(request.POST)
        if registration_form.is_valid():
            try:
                print('Registration form is valid. Attempting to save...')
                user = registration_form.save()
                login(request, user)
                return HttpResponse(status=200)
            except Exception as e:
                return HttpResponse(e)
        else:
            errors = registration_form.errors.as_text()
            print(errors)
            return HttpResponse(errors, status=500, content_type="text/html")

            # Redirect to the home page or any other page


def searchitems(request):
     query = request.GET.get('q')
     search_results = Product.objects.none()
     if query is not None:
         search_results = Product.objects.filter(title__icontains=query )
     registration_form = CustomUserCreationForm()
     login_form = CustomAuthenticationForm()
     all_categories = Category.objects.all()
     categories = Category.objects.filter(parent__isnull=True)
     context = {'categories': categories,  'reg_form': registration_form,
                'login_form': login_form, 'products': search_results, 'all_categories': all_categories}
     return render(request, 'search.html', context)

def aboutus(request):
    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()
    category_products = {}
    for category in all_categories:
        products = Product.objects.filter(category=category).order_by('-created')[:3]
        category_products[category] = products
    categories = Category.objects.filter(parent__isnull=True)
    context = {'categories': categories, 'category_products': category_products, 'reg_form': registration_form ,'login_form': login_form}
    return render(request, 'aboutus.html', context)

def updateitem(request):
    data = json.loads(request.body)
    productID = data['pid']
    action = data['action']
    print(productID)
    customer = request.user
    product = Product.objects.get(id=productID)
    order , created1 = Order.objects.get_or_create(customer=customer, status='cart')
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderitem.quantity +=1
        orderitem.save()
        print(orderitem.quantity)
        return JsonResponse({'quantity':orderitem.quantity, 'sum': orderitem.quantity*product.price}, safe=False)

    if action == 'remove':
        orderitem.quantity -=1
        if orderitem.quantity <= 0:
            orderitem.delete()
        else:
            orderitem.save()
        return JsonResponse({'quantity': orderitem.quantity, 'sum': orderitem.quantity * product.price}, safe=False)
    if orderitem.quantity <= 0 or action == 'delete':
        orderitem.delete()
        return JsonResponse({'quantity': 0, 'sum': orderitem.quantity * product.price}, safe=False)


    return JsonResponse('Item was added', safe=False)


def cart(request):
    order= Order.objects.get(customer=request.user, status='cart')
    print(order)
    cartitems = OrderItem.objects.filter(order=order)
    cartsum = 0
    for item in cartitems:
        cartsum += item.quantity*item.product.price
    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()
    category_products = {}
    for category in all_categories:
        products = Product.objects.filter(category=category).order_by('-created')[:3]
        category_products[category] = products
    categories = Category.objects.filter(parent__isnull=True)

    context = {'categories': categories, 'category_products': category_products, 'reg_form': registration_form,
               'login_form': login_form, 'cartitems':cartitems , 'total': cartsum}
    return render(request, 'cart.html', context )
