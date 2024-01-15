from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Owner


def ownerProfile(request, pk):
    owner = Owner.objects.get(pk=pk)
    animals = owner.animal_set.all()

    context = {
        "owner": owner,
        "animals": animals, 
    }
    return render(request, "owners/profile.html", context)
