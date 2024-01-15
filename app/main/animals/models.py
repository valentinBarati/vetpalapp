from django.db import models
from django.conf import settings
from owners.models import Owner


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Animal(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    operators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="operators", blank=True
    )
    animal_type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, null=True, blank=True
    )
    # image = models.ImageField(upload_to='animal_images/', null=True, blank=True)
    weight_kg = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    is_neutered = models.BooleanField(default=False)
    vaccination_records = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="created_animal",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="updated_animal",
    )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name
