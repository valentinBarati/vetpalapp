from django.urls import path
from . import views

app_name = 'samples'

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>/", views.sample, name="sample"),
    path("create/", views.createSample, name="create"),
    path("update/<int:pk>/", views.updateSample, name="update"),
    path("delete/<int:pk>/", views.deleteSample, name="delete"),
]
