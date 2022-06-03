from django.contrib import admin
from .models import Coupon

class OoderAdmin(admin.ModelAdmin):
    list_display = ('code', 'value','active','num_available','num_used')
    list_display_links = ('code', )
    search_fields = ('code',)
    list_editable= ['value','active','num_available']
    list_per_page = 25

admin.site.register(Coupon,OoderAdmin)