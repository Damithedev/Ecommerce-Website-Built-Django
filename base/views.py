import json
import threading
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from Tag import settings
from base.forms import CustomAuthenticationForm, CustomUserCreationForm
from base.models import Category, Product, ProductImages, Order, OrderItem,Customer,Address

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.views import APIView
from Tag.serializers import Orderserializer
from rest_framework import generics, status
from rest_framework.response import Response
import asyncio
def send_email(subject, message, recipients, template_path, context):
    # Render HTML content from the template and context
    html_content = render_to_string(template_path, context)
    # Send the email


    send_mail(
        subject=subject,
        message=message,  # Plain text version (can be an empty string)
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        html_message=html_content  # Attach the HTML content
    )

def send_email_wrapper(*args, **kwargs):
    # This wrapper function will run send_email in a separate thread
    email_thread = threading.Thread(target=send_email, args=args, kwargs=kwargs)
    email_thread.start()


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
    print("daiii")
    print(productID)
    product = Product.objects.get(id=productID)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, status='cart')
    else:
        guest_user, created = Customer.objects.get_or_create(username='guest')
        customer = guest_user
        cart_id = request.session.get('cart_id')

        if cart_id is None:
            order = Order.objects.create(customer=customer, status='cart')
            request.session['cart_id'] = order.id
        else:
            try:
                order = Order.objects.get(customer=customer, status='cart', id=cart_id)
            except Order.DoesNotExist:
                order = Order.objects.create(customer=customer, status='cart')
                request.session['cart_id'] = order.id


    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderitem.quantity +=1
        if orderitem.quantity > product.quantity:
            return JsonResponse({'response': 'Max quantity exceeded'})
        orderitem.save()


        cartitems = OrderItem.objects.filter(order=order)
        cartsum = 0
        for item in cartitems:
            cartsum += item.quantity * item.product.price
        return JsonResponse({'quantity':orderitem.quantity, 'sum': orderitem.quantity*product.price, 'cartsum': cartsum, 'response': 'success'}, safe=False)

    if action == 'remove':
        orderitem.quantity -=1
        if orderitem.quantity <= 0:
            orderitem.delete()
        else:
            orderitem.save()
        cartitems = OrderItem.objects.filter(order=order)
        cartsum = 0
        for item in cartitems:
            cartsum += item.quantity * item.product.price
        return JsonResponse({'quantity': orderitem.quantity, 'sum': orderitem.quantity * product.price, 'cartsum': cartsum, 'response': 'success'}, safe=False)
    if orderitem.quantity <= 0 or action == 'delete':
        orderitem.delete()
        cartitems = OrderItem.objects.filter(order=order)
        cartsum = 0
        for item in cartitems:
            cartsum += item.quantity * item.product.price
        return JsonResponse({'quantity': 0, 'sum': orderitem.quantity * product.price, 'cartsum': cartsum, 'response': 'success'}, safe=False)


    return JsonResponse('Item was added', safe=False)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, status='cart')
    else:
        guest_user, created = Customer.objects.get_or_create(username='guest')
        customer = guest_user
        cart_id = request.session.get('cart_id')

        if cart_id is None:
            order = Order.objects.create(customer=customer, status='cart')
            request.session['cart_id'] = order.id
        else:
            try:
                order = Order.objects.get(customer=customer, status='cart', id=cart_id)
            except Order.DoesNotExist:
                order = Order.objects.create(customer=customer, status='cart')
                request.session['cart_id'] = order.id

    print(order)

    cartitems = OrderItem.objects.filter(order=order)
    cartsum = 0
    for item in cartitems:
        cartsum += item.quantity * item.product.price

    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()
    category_products = {}
    for category in all_categories:
        products = Product.objects.filter(category=category).order_by('-created')[:3]
        category_products[category] = products
    categories = Category.objects.filter(parent__isnull=True)
    order.subtotal = cartsum
    order.save()

    context = {
        'categories': categories,
        'category_products': category_products,
        'reg_form': registration_form,
        'login_form': login_form,
        'cartitems': cartitems,
        'total': cartsum
    }

    return render(request, 'cart.html', context)

@login_required
def checkout(request):
    order = Order.objects.get(customer=request.user, status='cart')
    cartitems = OrderItem.objects.filter(order=order)
    print(order)


    cartsum = order.subtotal
    if request.method == 'POST':
        print(request.POST)
        user = request.user
        if user.first_name == '' or user.first_name is None:
            first_name = request.POST['firstname']
            last_name =request.POST['lastname']
            phone = request.POST['phone']
            email = request.POST['email']

            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.email = email
            user.save()
        delivery_option = request.POST['deliveryoption']
        if delivery_option == 'delivery':
            order.total = order.subtotal + 2000
            order.shipping_fee = 2000
            order.save()
        else:
            order.shipping_fee = 0
            order.total = order.subtotal
        addressinput = request.POST['address']
        city = request.POST['city']
        msgforseller = request.POST['msgsell']
        address, created = Address.objects.get_or_create(customer=user)
        address.address = addressinput
        address.city = city
        address.save()
        order.status = "Recieved"
        order.deliverymethod = delivery_option
        order.address = address
        order.date = datetime.now()
        order.save()
        for item in cartitems:

            item.product.quantity -= item.quantity
            item.product.save()
            print(f'item:{item.product.quantity}')
        return redirect('invoice', oid = order.id)

    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()
    category_products = {}
    for category in all_categories:
        products = Product.objects.filter(category=category).order_by('-created')[:3]
        category_products[category] = products
    categories = Category.objects.filter(parent__isnull=True)

    context = {'categories': categories, 'category_products': category_products, 'reg_form': registration_form,
               'login_form': login_form, 'cartitems': cartitems, 'total': cartsum}


    return render(request, 'checkout.html', context)

@login_required
def invoice(request, oid):
    order = Order.objects.get(customer=request.user, id = oid)
    print(order)
    cartitems = OrderItem.objects.filter(order=order)
    cartsum = order.subtotal
    total = order.total
    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()
    category_products = {}
    for category in all_categories:
        products = Product.objects.filter(category=category).order_by('-created')[:3]
        category_products[category] = products
    categories = Category.objects.filter(parent__isnull=True)

    context = { 'categories': categories, 'category_products': category_products, 'reg_form': registration_form,
               'login_form': login_form, 'cartitems': cartitems, 'subtotal': cartsum , 'orders': order , 'total': total}
    send_email_wrapper("Hello", "Hello world", [order.customer.email],
                       template_path='/home/damilola/Documents/django projecta/Ecommerce-Website-Built-Django/templates/email.html',
                       context=context)
    return render(request, 'order.html', context)

class OrderList(generics.ListCreateAPIView):
    def get(self, request, format=None):
        orders = Order.objects.filter(status = 'Recieved')
        serializer = Orderserializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
