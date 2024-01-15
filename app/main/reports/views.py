from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from wkhtmltopdf.views import PDFTemplateView
from animals.models import Animal
from datetime import datetime
from base.decorators import check_user_permission
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class AnimalPDFView(PDFTemplateView):
    template_name = "reports/report.html"

    @method_decorator(user_passes_test(lambda u: u.is_authenticated and u.is_veterinarian))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        animal_id = self.kwargs.get("animal_id")
        animal = Animal.objects.get(id=animal_id)

        current_date = datetime.now().strftime("%Y-%m-%d")
        self.filename = f"{animal.name}_{current_date}_animal_summary.pdf"
        return {"animal": animal}
