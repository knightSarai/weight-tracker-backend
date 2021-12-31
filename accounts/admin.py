from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', 'firstname', 'lastname',)
    list_filter = ('email', 'username', 'firstname', 'lastname', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = (
        'id', 'email', 'username', 'firstname', 'lastname', 'is_active', 'is_staff'
    )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'firstname', 'lastname',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'firstname', 'lastname', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)
