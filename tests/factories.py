# https://faker.readthedocs.io/en/latest/providers/faker.providers.person.html
from random import choice, uniform

from django.contrib.gis.geos import Point

from factory import (
    DjangoModelFactory, Faker, PostGenerationMethodCall,
    RelatedFactory, SubFactory,
)
from factory.fuzzy import BaseFuzzyAttribute

from hosting.models import MR, MRS, PRONOUN_CHOICES

from .constants import PERSON_LOCALES


class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(uniform(-180.0, 180.0), uniform(-90.0, 90.0))


class LocaleFaker(Faker):
    @classmethod
    def _get_faker(cls, locale=None):
        return super()._get_faker(locale=choice(PERSON_LOCALES))


class AgreementFactory(DjangoModelFactory):
    class Meta:
        model = "core.Agreement"

    user = SubFactory("tests.factories.UserFactory", agreement=None)
    policy_version = "2018-001"
    withdrawn = None


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "auth.User"

    username = Faker("user_name")
    password = PostGenerationMethodCall("set_password", "adm1n")
    first_name = ""
    last_name = ""
    email = Faker("email")
    is_active = True
    is_staff = False

    profile = RelatedFactory("tests.factories.ProfileFactory", "user")
    agreement = RelatedFactory(AgreementFactory, "user")


class StaffUserFactory(UserFactory):
    is_staff = True


class AdminUserFactory(StaffUserFactory):
    is_superuser = True


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = "hosting.Profile"
        django_get_or_create = ("user",)

    user = SubFactory("tests.factories.UserFactory", profile=None)
    title = Faker("random_element", elements=[MRS, MR])
    first_name = LocaleFaker("first_name")
    last_name = LocaleFaker("last_name")
    names_inversed = False
    pronoun = Faker(
        "random_element", elements=[ch[0] for ch in PRONOUN_CHOICES if ch[0]]
    )
    birth_date = Faker("date_between", start_date="-100y", end_date="-18y")
    description = Faker("sentence")


class PlaceFactory(DjangoModelFactory):
    class Meta:
        model = "hosting.Place"

    owner = SubFactory("tests.factories.ProfileFactory")

    address = Faker("street_address")
    city = Faker("city")
    closest_city = Faker("city")
    postcode = Faker("postcode")
    state_province = Faker("state")
    country = Faker("country_code")
    location = FuzzyPoint()
    location_confidence = Faker("pyint")
    max_guest = Faker("pyint")
    max_night = Faker("pyint")
    contact_before = Faker("pyint")
    description = Faker("text")
    short_description = Faker("bs")
    available = True
    in_book = True
    tour_guide = True
    have_a_drink = True
    sporadic_presence = False


    # conditions = models.ManyToManyField
    # family_members = models.ManyToManyField
    # family_members_visibility = models.OneToOneField
    blocked_from = None
    blocked_until = None
    # authorized_users = models.ManyToManyField
    # visibility = models.OneToOneField
