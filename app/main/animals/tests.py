from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from animals.models import Animal, Type
from animals.forms import AnimalForm
from owners.models import Owner
from base.models import VeterinarianUser


class AnimalViewTests(TestCase):
    def setUp(self):
        self.user = VeterinarianUser.objects.create_user(
            username="testuser", password="testpassword", is_superuser=True
        )

        self.animal_type = Type.objects.create(name="Test Type")
        self.owner = Owner.objects.create(name="Test Owner", created_by=self.user)

    def test_create_animal_view_get(self):
        # Test the view for a GET request
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("animals:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/components/form.html")
        self.assertIsInstance(response.context["form"], AnimalForm)

    def test_create_animal_view_post(self):
        # Test the view for a POST request with valid data
        self.client.login(username="testuser", password="testpassword")

        form_data = {
            "name": "Test Animal",
            "animal_type": self.animal_type.pk,
            "owner": self.owner.pk,
            "created_by": self.user.pk,
        }
        response = self.client.post(reverse("animals:create"), data=form_data)

        # Check if the animal is created in the database
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(Animal.objects.count(), 1)
        new_animal = Animal.objects.first()
        self.assertEqual(new_animal.name, "Test Animal")
        # Add assertions for other fields

        # Check if the user is set as the creator
        self.assertEqual(new_animal.created_by, self.user)

        # Check if the user is redirected to the correct page
        self.assertRedirects(
            response, reverse("animals:animal", kwargs={"pk": new_animal.pk})
        )
