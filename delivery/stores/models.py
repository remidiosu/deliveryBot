from django.db import models
from users.models import TimeStampedUUIDModel

class Store(TimeStampedUUIDModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    working_hours = models.CharField(max_length=500)
    notes = models.TextField(blank=True, null=True)

    class Meta(TimeStampedUUIDModel.Meta):
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class StoreAddress(TimeStampedUUIDModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="addresses")
    address_line = models.CharField(max_length=300)
    additional_desc = models.TextField(max_length=1000)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_primary = models.BooleanField(default=True)

    class Meta(TimeStampedUUIDModel.Meta):
        indexes = [models.Index(fields=["is_primary"])]

    def __str__(self):
        return f"{self.store.name}: {self.address_line}"


class StoreContact(TimeStampedUUIDModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="contacts")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=32)  
    position = models.CharField(max_length=120, blank=True, null=True)
    is_primary = models.BooleanField(default=True)

    class Meta(TimeStampedUUIDModel.Meta):
        indexes = [models.Index(fields=["is_primary"])]

    def __str__(self):
        return f"{self.store.name}: {self.full_name}"


class StorePaymentTerm(TimeStampedUUIDModel):
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name="payment_term")
    accepts_cash = models.BooleanField(default=True)
    accepts_card = models.BooleanField(default=True)
    deferred_allowed = models.BooleanField(default=False)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2)
