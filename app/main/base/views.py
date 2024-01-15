from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from animals.models import Animal, Owner
from samples.models import Sample
from django.contrib.auth import authenticate, login, logout
from .forms import VeterinarianUserCreationForm


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = get_user_model().objects.get(username=username)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Username OR password is incorrect")
        except:
            messages.error(request, "Username does not exist")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


def registerPage(request):
    form = VeterinarianUserCreationForm()

    if request.method == "POST":
        form = VeterinarianUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to database yet
            user.username = user.username.lower()
            user.save()
            login(request, user)

            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    context = {"form": form}
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    animals = Animal.objects.filter(
        Q(id__icontains=q)
        | Q(owner__name__icontains=q)
        | Q(name__icontains=q)
        | Q(animal_type__name__icontains=q)
        | Q(description__icontains=q)
    )
    if q == "":
        animals = animals.order_by("-created")[0:25]

    owners = Owner.objects.filter(
        Q(name__icontains=q)
        | Q(id__icontains=q)
        | Q(phone_number__icontains=q)
        | Q(email__icontains=q)
    )
    recent_activities = []

    if request.user != None and request.user.is_authenticated:
        recent_activities = Sample.objects.filter(
            Q(animal__operators=request.user) | Q(created_by=request.user)
        ).order_by("-created")[0:5]

    context = {
        "animals": animals,
        "owners": owners,
        "recent_activities": recent_activities,
    }
    return render(request, "base/home.html", context)


def userProfile(request, pk):
    profile = get_user_model().objects.get(id=pk)

    operators_animals = Animal.objects.filter(operators=profile)
    own_animals = Animal.objects.filter(created_by=profile)
    animals = operators_animals | own_animals
    owners = Owner.objects.filter(animal__in=animals).distinct()
    samples = Sample.objects.filter(created_by=profile)
    recent_activities = Sample.objects.filter(created_by=profile).order_by("-created")[
        0:5
    ]

    context = {
        "profile": profile,
        "animals": animals,
        "samples": samples,
        "owners": owners,
        "recent_activities": recent_activities,
    }
    return render(request, "base/profile.html", context)
