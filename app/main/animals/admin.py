from django.contrib import admin

# Register your models here.

from .models import Type, Animal

admin.site.register(Type)
admin.site.register(Animal)