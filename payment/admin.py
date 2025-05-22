from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User


admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#create an order item Inline
class OrderItemInLine(admin.StackedInline):
    model=OrderItem
    extra = 0

#extend our order model
class OrderAdmin(admin.ModelAdmin):
    model=Order
    readonly_fields = ["date_orderd"]
    inlines=[OrderItemInLine]

#unregister order moder
admin.site.unregister(Order)

#re-register our order and the order item
admin.site.register(Order,OrderAdmin)