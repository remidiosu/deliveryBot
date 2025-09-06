from django.contrib import admin
from .models import Courier, Controller

    
@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ("full_name", "telegram_id", "phone_number", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "phone_number", "telegram_id") 


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "telegram_id", "phone_number", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "phone_number", "telegram_id")
