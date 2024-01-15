from django.db import models
from django.conf import settings


class Owner(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    co_owners = models.ManyToManyField("self", related_name="co_owners", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="created_owner",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="updated_owner",
    )
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
