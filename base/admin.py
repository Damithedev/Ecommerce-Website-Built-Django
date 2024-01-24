from django.contrib import admin
from base.models import Category, Product, ProductImages,Order,OrderItem,Address,Customer
from base.views import send_email

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
    list_display = ('id', 'customer', 'status', 'date', 'deliverymethod', 'subtotal', 'total', 'shipping_fee')
    list_filter = ('status',)
    actions = ['accept_orders', 'decline_orders']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(status='Recieved')
    def accept_orders(self, request, queryset):
        queryset.update(status='Accepted')
        for order in queryset:
            print(order)
            cartitems = OrderItem.objects.filter(order=order)
            cartsum = order.subtotal
            total = order.total



            context = { 'cartitems': cartitems, 'subtotal': cartsum, 'orders': order, 'status': order.status,
                   'total': total}
            send_email("Hello", "Hello world", [order.customer.email],
                   template_path='/home/damilola/PycharmProjects/Tag/templates/email.html', context=context)


    def decline_orders(self, request, queryset):
        queryset.update(status='Declined')


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

class Addresses(admin.TabularInline):
    model = Address


class CustomerAdmin(admin.ModelAdmin):
    inlines = [Addresses]

admin.site.register(Customer, CustomerAdmin)

