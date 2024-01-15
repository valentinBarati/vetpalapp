# myapp/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker
from animals.models import Type as AnimalType, Animal
from samples.models import Type as SampleType, Sample
from base.models import VeterinarianUser
from owners.models import Owner
from django.contrib.auth import get_user_model
from django.utils import timezone


class Command(BaseCommand):
    help = "Seed data for Owners, Animal Type and Animal models"

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        faker = Faker()

        # Create a default user
        default_user = VeterinarianUser.objects.create(
            username="test", email="test@example.com", is_superuser=True
        )
        default_user.set_password("test")
        default_user.save()

        seeder.add_entity(VeterinarianUser, 5)

        users = get_user_model().objects.all()

        # Seed data for Owners
        seeder.add_entity(
            Owner,
            15,
            {
                "name": lambda x: seeder.faker.name(),
                "email": lambda x: seeder.faker.email(),
                "phone_number": lambda x: seeder.faker.numerify(text="###########"),
                "address": lambda x: seeder.faker.address(),
                "emergency_contact_name": lambda x: seeder.faker.name(),
                "emergency_contact_phone": lambda x: seeder.faker.numerify(
                    text="###########"
                ),
                "notes": lambda x: seeder.faker.text(),
                "created_by": lambda x: seeder.faker.random_element(elements=users),
                "updated_by": lambda x: seeder.faker.random_element(elements=users),
            },
        )

        # Seed data for Animals
        owners = Owner.objects.all()

        seeder.add_entity(
            AnimalType,
            3,
            {
                "name": lambda x: faker.word().capitalize(),
            },
        )

        animal_types = AnimalType.objects.all()

        seeder.add_entity(
            Animal,
            35,
            {
                "name": lambda x: seeder.faker.first_name(),
                "owner": lambda x: seeder.faker.random_element(elements=owners),
                "description": lambda x: seeder.faker.text(),
                "birth_date": lambda x: seeder.faker.date_of_birth(),
                "animal_type": lambda x: seeder.faker.random_element(
                    elements=animal_types
                ),
                "weight_kg": lambda x: seeder.faker.random_element(
                    elements=(None, seeder.faker.random_number(1, 2))
                ),
                "height_cm": lambda x: seeder.faker.random_element(
                    elements=(None, seeder.faker.random_number(1, 3))
                ),
                "is_neutered": (
                    lambda x: seeder.faker.random_element(elements=(True, False))
                ),
                "vaccination_records": lambda x: seeder.faker.text(),
                "notes": lambda x: seeder.faker.text(),
                "created_by": lambda x: seeder.faker.random_element(elements=users),
                "updated_by": lambda x: seeder.faker.random_element(elements=users),
            },
        )

        seeder.add_entity(
            SampleType,
            5,
            {
                "name": lambda x: faker.word().capitalize(),
            },
        )

        sample_types = SampleType.objects.all()
        animals = Animal.objects.all()

        seeder.add_entity(
            Sample,
            150,
            {
                "name": lambda x: faker.word().capitalize(),
                "animal": lambda x: seeder.faker.random_element(animals),
                "description": lambda x: faker.text(),
                "sample_type": lambda x: seeder.faker.random_element(sample_types),
                "collection_date": lambda x: seeder.faker.date_time_between(
                    start_date="-30d",
                    end_date="now",
                    tzinfo=timezone.get_current_timezone(),
                ),
                "analysis_results": lambda x: faker.text(),
                "is_approved": lambda x: faker.boolean(),
                "created_by": lambda x: seeder.faker.random_element(users),
                "updated_by": lambda x: seeder.faker.random_element(users),
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Data seeded successfully!"))
