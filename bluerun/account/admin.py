from django.contrib import admin
from .models import MyUser, UserOTP
from django.contrib.auth.models import Group

# Register your models here.
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email']

admin.site.unregister(Group)