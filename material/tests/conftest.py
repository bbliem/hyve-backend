import pytest
from rest_framework.test import APIClient

from material.models import Organization, User


@pytest.fixture
def admin(db):
    return User.objects.create(email='admin@example.com', is_superuser=True)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def organization(db):
    return Organization.objects.create(name='Organization')


@pytest.fixture
def user(db, organization):
    return User.objects.create(email='user@example.com', organization=organization)


@pytest.fixture
def superuser(db, organization):
    return User.objects.create(email='superuser@example.com', is_superuser=True)


@pytest.fixture
def supervisor(db, organization):
    return User.objects.create(email='supervisor@example.com', organization=organization, is_supervisor=True)
