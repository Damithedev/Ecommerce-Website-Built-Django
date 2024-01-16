from django.contrib import admin
from base.models import Category, Product, ProductImages
admin.site.register(Category)
# Register your models here.
class ProductImageInline(admin.TabularInline):  # TabularInline or StackedInline based on your preference
    model = ProductImages
    extra = 3  # Number of empty image slots to show by default

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)

