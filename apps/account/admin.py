from django.contrib import admin

from .models import UserProfile,UserAddress


class AddressItemInline(admin.StackedInline):
    
    model=UserAddress
    fields =['first_name', 'last_name','enterprise','address','city','district','zipcode','phone']
    

class UserProfileAdmin(admin.ModelAdmin):
  
    inlines=[AddressItemInline]
    
    list_display = ('user', 'treatment', 'phone', 'dni', )
    list_display_links = ('user', )
    list_editable = ('phone', )
    list_per_page = 25
admin.site.register(UserProfile, UserProfileAdmin)
