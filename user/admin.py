from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'last_name', 'first_name', 'middle_name',  'is_active',
                    'is_superuser', 'is_staff', 'date_joined', 'last_login']
    list_display_links = ['role', 'last_name', 'first_name', 'middle_name', ]
    list_filter = ['role', 'is_active', ]
    search_fields = ['last_name', 'first_name', 'middle_name', 'username',  ]
    save_on_top = True
