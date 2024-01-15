from django.db import models
from animals.models import Animal
from django.conf import settings
from django.utils import timezone


class Type(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Sample(models.Model):
    name = models.CharField(max_length=150)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    sample_type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, null=True, blank=True
    )
    collection_date = models.DateTimeField(default=timezone.now)
    analysis_results = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="collected_samples",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_samples",
    )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name
