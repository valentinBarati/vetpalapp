from django.urls import path
from .views import AnimalPDFView

app_name = 'reports'

urlpatterns = [
    path('<int:animal_id>', AnimalPDFView.as_view(), name='summary'),
]