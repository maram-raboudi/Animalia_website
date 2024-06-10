from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

#register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#create an orderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#extend our order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user","full_name","shipped","date_shipped"]
    inlines = [OrderItemInline]

#unregister Order Model
admin.site.unregister(Order)

#re-register our order and orderadmin
admin.site.register(Order, OrderAdmin)
    