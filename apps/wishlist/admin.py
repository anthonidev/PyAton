from django.contrib import admin

from .models import WishList,WishListItem


class WishItemInline(admin.TabularInline):
    model=WishListItem
    fields =['product',]
class WishAdmin(admin.ModelAdmin):
    list_display=['user',]
    inlines=[WishItemInline]

admin.site.register(WishList,WishAdmin)
