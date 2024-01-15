from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from animals.models import Animal
from .models import Sample
from .forms import SampleForm
from base.decorators import check_user_permission


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    samples = Sample.objects.filter(
        Q(id__icontains=q)
        | Q(name__icontains=q)
        | Q(sample_type__name__icontains=q)
        | Q(description__icontains=q)
        | Q(analysis_results__icontains=q)
    ).order_by("-created")

    context = {"samples": samples}
    return render(request, "samples/home.html", context)


def sample(request, pk):
    sample = Sample.objects.get(pk=pk)
    context = {"sample": sample}
    return render(request, "samples/sample.html", context)


@check_user_permission("samples.add_animal")
def createSample(request):
    form = SampleForm()
    if request.method == "POST":
        print(request.POST)
        form = SampleForm(request.POST)
        if form.is_valid():
            prepare = form.save(commit=False)
            prepare.created_by = request.user
            prepare.save()
            animal = Animal.objects.get(pk=prepare.animal.id)
            animal.operators.add(request.user)

            previous_page = request.META.get("HTTP_REFERER", "/")
            return redirect("animals:animal", pk=prepare.animal.id)
    context = {
        "title": "Create Sample",
        "method": "post",
        "action": reverse("samples:create"),
        "form": form,
    }
    return render(request, "base/components/form.html", context)


@check_user_permission("samples.change_animal")
def updateSample(request, pk):
    sample = Sample.objects.get(pk=pk)
    form = SampleForm(instance=sample)
    if request.method == "POST":
        form = SampleForm(request.POST, instance=sample)
        if form.is_valid():
            form.save()
            prepare = form.save(commit=False)
            prepare.updated_by = request.user
            prepare.save()
            return redirect("samples:sample", pk=prepare.id)
    context = {
        "title": "Edit Sample: " + sample.name,
        "method": "post",
        "action": reverse("samples:update", kwargs={"pk": pk}),
        "form": form,
    }
    return render(request, "base/components/form.html", context)


@check_user_permission("samples.delete_animal")
def deleteSample(request, pk):
    sample = Sample.objects.get(pk=pk)

    if request.method == "POST":
        sample.delete()
        return redirect("home")
    context = {"sample": sample}
    return render(request, "base/components/delete.html", {"obj": sample})
