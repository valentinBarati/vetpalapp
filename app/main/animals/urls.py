from django.urls import path
from . import views

app_name = 'animals'

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>/", views.animal, name="animal"),
    path("create/", views.createAnimal, name="create"),
    path("update/<int:pk>/", views.updateAnimal, name="update"),
    path("delete/<int:pk>/", views.deleteAnimal, name="delete"),
]
