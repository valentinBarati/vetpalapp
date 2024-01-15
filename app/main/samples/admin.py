from django.contrib import admin

# Register your models here.

from .models import Sample, Type

admin.site.register(Sample)
admin.site.register(Type)