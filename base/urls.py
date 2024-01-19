from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pid>', views.product, name='product details'),
    path('category/<int:cid>', views.category_page, name='category details'),
    path('search', views.searchitems, name='search'),
    path('about', views.aboutus, name='about'),
    path('updateitem', views.updateitem, name='updateitem'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout')
    ]