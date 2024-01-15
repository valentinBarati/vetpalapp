from django.contrib import admin

# Register your models here.

from .models import VeterinarianUser, Permission

admin.site.register(Permission)
admin.site.register(VeterinarianUser)