from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    description = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Use auto_now_add for creation date
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cashondelivery = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.title

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/', blank=True)  # Use a more suitable upload_to path

class Customer(AbstractUser):
    phone = models.CharField(max_length=11, null=True, blank=True)
    created = models.DateField(auto_now_add=True)  # Use auto_now_add for creation date
    address = models.CharField(max_length=2000, null=True, blank=True)


    def __str__(self):
        return self.username


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=19)
    date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
