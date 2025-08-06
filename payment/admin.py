from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.// register the models on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# Creat an orderitem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#Extend Our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['user','full_name','email','shipping_address','amount_paid','date_ordered','shipped','date_shipped']
    inlines = [OrderItemInline]

#Unregister Order Model
admin.site.unregister(Order)


#reregister our order and orderAdmin
admin.site.register(Order, OrderAdmin)

