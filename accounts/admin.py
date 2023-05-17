from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import CustomUser


class UserAdmin(BaseUserAdmin):
  

    list_display = ('username', 'phone_number', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')
    readonly_fields = ('last_login', )

    fieldsets = (
        (None, {"fields": (
            'username', 'phone_number', 'email', 'address', 'post_code', 'profile_image',
        'password')
        }),
        ('permissions', {"fields": ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {"fields": ('username', 'phone_number', 'email', 'password1', 'password2')}),
    )

    search_fields = ('username', 'phone_number', 'email')
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            field = form.base_fields.get('is_superuser')
            if field:
                field.disabled = True
        return form


admin.site.register(CustomUser, UserAdmin)