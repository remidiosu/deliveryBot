from rest_framework import serializers
from .models import Courier, Controller


class CourierSerializer(serializers.ModelSerializer):
    controller_id = serializers.PrimaryKeyRelatedField(
        source="controller",
        queryset=Controller.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Courier
        fields = ["id", "full_name", "telegram_id", "phone_number", "controller_id", "is_active"]
        read_only_fields = ["id", "is_active"]


class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controller
        fields = ["id", "full_name", "telegram_id", "phone_number", "is_active"]
        read_only_fields = ["id", "is_active"]
