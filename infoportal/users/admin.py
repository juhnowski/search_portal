from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Company


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name',
                    'patronymic', 'role', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('password', )}),
        ('Персональная информация', {'fields': ('first_name',
                                                'last_name',
                                                'patronymic',
                                                'email',
                                                'phone',
                                                'role',
                                                'company',
                                                )
                                     }),
        ('Данные', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company, CompanyAdmin)
