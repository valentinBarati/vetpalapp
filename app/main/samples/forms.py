from django import forms
from django.forms import ModelForm
from .models import Sample

class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        exclude = ['created_by', 'updated_by']