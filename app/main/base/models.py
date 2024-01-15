from django.db import models
from django.contrib.auth.models import AbstractUser
from animals.models import Animal
from django.contrib.auth.models import Group, Permission


class VeterinarianUser(AbstractUser):
    is_veterinarian = models.BooleanField(default=False)
