from rest_framework import serializers
from .models import Courier, Controller

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ["id", "full_name", "telegram_id", "phone_number", "organization", "is_active"]
        read_only_fields = ["id", "organization", "is_active"]

class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controller
        fields = ["id", "full_name", "telegram_id", "phone_number", "organization", "is_active"]
        read_only_fields = ["id", "organization", "is_active"]