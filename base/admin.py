from django.contrib import admin
from base.models import Category, Product, ProductImages,Order,OrderItem,Address,Customer
admin.site.register(Category)
# Register your models here.
class ProductImageInline(admin.TabularInline):  # TabularInline or StackedInline based on your preference
    model = ProductImages
    extra = 3  # Number of empty image slots to show by default

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class Orderitemslist(admin.TabularInline):
    model = OrderItem
class OrderAdmin(admin.ModelAdmin):
    inlines = [Orderitemslist]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

class Addresses(admin.TabularInline):
    model = Address


class CustomerAdmin(admin.ModelAdmin):
    inlines = [Addresses]

admin.site.register(Customer, CustomerAdmin)

