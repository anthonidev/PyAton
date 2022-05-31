from django.contrib import admin

from .models import UserProfile,UserAddress

admin.site.register(UserProfile)
admin.site.register(UserAddress)