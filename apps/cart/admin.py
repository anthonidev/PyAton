from django.contrib import admin

from .models import Cart,CartItem


class CartItemInline(admin.TabularInline):
    model=CartItem
    fields =['product', 'count']
class CartAdmin(admin.ModelAdmin):
    list_display=['user',]
    inlines=[CartItemInline]

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem)