from django.contrib import admin
from .models import Payment, Order, OrderedFood



class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0
    
class OrderFoodadmin(admin.ModelAdmin):
    list_display = ['order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount']
    search_fields = ['order__order_number']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'order_placed_to', 'is_ordered']
    inlines = [OrderedFoodInline]




admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood, OrderFoodadmin)


