from django.contrib import admin
from .models import Organization, Courier, Controller

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",) 
    
@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ("full_name", "organization", "telegram_id", "phone_number", "is_active")
    list_filter = ("organization", "is_active")
    search_fields = ("full_name", "phone_number", "telegram_id") 
    autocomplete_fields = ("organization",)

@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "organization", "telegram_id", "phone_number", "is_active")
    list_filter = ("organization", "is_active")
    search_fields = ("full_name", "phone_number", "telegram_id")
    autocomplete_fields = ("organization",)
