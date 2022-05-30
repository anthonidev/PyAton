
from django.contrib import admin

from apps.product.models import Category, Product, Brand, CharacteristicProduct, ProductImage


class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','parent')
    list_display_links = ('title','parent' )
    search_fields = ('title',)
    list_per_page = 25
    
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand','price','quantity','category')
    list_display_links = ('title','brand','category' )
    search_fields = ('title','slugh','brand','category')
    list_per_page = 25
class CharacteristicItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'title','description')
    list_display_links = ('product','title', )
    list_per_page = 25


admin.site.register(Category, CategoryItemAdmin)
admin.site.register(Product, ProductItemAdmin)
admin.site.register(CharacteristicProduct,CharacteristicItemAdmin)


admin.site.register(Brand)
admin.site.register(ProductImage)
