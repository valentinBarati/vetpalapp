from django.urls import path
from . import views

app_name = 'owners'

urlpatterns = [
    path("<int:pk>/", views.ownerProfile, name="profile"),
]

