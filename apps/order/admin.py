from django.contrib import admin

from apps.order.models import Order, OrderItem
class OrderItemAdmin(admin.ModelAdmin):
    # def has_delete_permission(self, request, obj=None):
    #     return False

    list_display = ('id', 'name', 'price', 'count', )
    list_display_links = ('id', 'name', )
    list_per_page = 25

class OrderItemInline(admin.StackedInline):
    
    model=OrderItem
    readonly_fields =('product', 'count','price','date_added',)
    
    
class OrderAdmin(admin.ModelAdmin):
    # def has_delete_permission(self, request, obj=None):
    #     return False
    inlines=[OrderItemInline]
    
    list_display = ('id', 'transaction_id', 'amount', 'status', )
    list_display_links = ('id', 'transaction_id', )
    list_filter = ('status', )
    list_editable = ('status', )
    list_per_page = 25


admin.site.register(Order, OrderAdmin)


