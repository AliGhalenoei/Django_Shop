from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .forms import *
# Register your models here.

class UserAdmin(BaseUserAdmin):
    form=UserChangeForm
    add_form=UserCreationForm

    fieldsets=(
        (None,{'fields':('phone','email','username','password')}),
        ('Status',{'fields':('is_admin','is_active')}),
        ('Time',{'fields':('last_login',)}),
    )

    add_fieldsets=(
        (None,{'fields':('phone','email','username','password','password2')}),
    )

    list_display=('username','phone','email','is_admin')
    list_filter=('last_login',)
    search_fields=('username',)
    filter_horizontal=()
    ordering=('username',)

admin.site.unregister(Group)
admin.site.register(User,UserAdmin)

admin.site.register(OTP)

