from django.contrib import admin

from apps.public.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", "date_joined", "is_active"]
