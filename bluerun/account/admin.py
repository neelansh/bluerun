from django.contrib import admin
from .models import MyUser, UserOTP

# Register your models here.
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

admin.site.register(UserOTP)