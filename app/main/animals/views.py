from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from base.decorators import check_user_permission
from django.db.models import Q
from .models import Animal
from .forms import AnimalForm
from samples.forms import SampleForm
from django import forms


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    animals = Animal.objects.filter(
        Q(id__icontains=q)
        | Q(owner__name__icontains=q)
        | Q(name__icontains=q)
        | Q(animal_type__name__icontains=q)
        | Q(notes__icontains=q)
        | Q(description__icontains=q)
    )

    context = {"animals": animals}
    return render(request, "animals/home.html", context)


def animal(request, pk):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    animal = Animal.objects.get(pk=pk)
    samples = animal.sample_set.filter(
        Q(id__icontains=q)
        | Q(name__icontains=q)
        | Q(sample_type__name__icontains=q)
        | Q(description__icontains=q)
        | Q(analysis_results__icontains=q)
    ).order_by("-created")

    sample_form = SampleForm()
    sample_form.fields["animal"].initial = animal
    sample_form.fields["animal"].widget = forms.HiddenInput()

    operators = animal.operators.all()

    context = {
        "animal": animal,
        "samples": samples,
        "operators": operators,
        "sample_form": sample_form,
    }
    return render(request, "animals/animal.html", context)


@check_user_permission("animals.add_animal")
def createAnimal(request):
    form = AnimalForm()
    if request.method == "POST":
        print(request.POST)
        form = AnimalForm(request.POST)
        if form.is_valid():
            prepare = form.save(commit=False)
            prepare.created_by = request.user
            prepare.save()
            return redirect("animals:animal", pk=prepare.id)
    context = {
        "title": "Create Animal",
        "method": "post",
        "action": reverse("animals:create"),
        "form": form,
    }
    return render(request, "base/components/form.html", context)


@check_user_permission("animals.change_animal")
def updateAnimal(request, pk):
    animal = Animal.objects.get(pk=pk)
    form = AnimalForm(instance=animal)
    if request.method == "POST":
        form = AnimalForm(request.POST, instance=animal)
        prepare = form.save(commit=False)
        prepare.updated_by = request.user
        prepare.save()
        return redirect("animals:animal", pk=prepare.id)
    context = {
        "title": "Edit Animal: " + animal.name,
        "method": "post",
        "action": reverse("animals:update", kwargs={"pk": pk}),
        "form": form,
    }
    return render(request, "base/components/form.html", context)


@check_user_permission("animals.delete_animal")
def deleteAnimal(request, pk):
    animal = Animal.objects.get(pk=pk)
    if request.method == "POST":
        animal.delete()
        return redirect("home")
    context = {"animal": animal}
    return render(request, "base/components/delete.html", {"obj": animal})
