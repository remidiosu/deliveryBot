import uuid
from django.db import models 


class TimeStampedUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Controller(TimeStampedUUIDModel): 
    full_name = models.CharField(max_length=200) 
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True) 
    phone_number = models.CharField(max_length=16, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self): 
        return self.full_name


class Courier(TimeStampedUUIDModel):
    full_name = models.CharField(max_length=200)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=16, unique=True, null=True, blank=True)
    controller = models.ForeignKey(
        Controller,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="couriers"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.full_name
