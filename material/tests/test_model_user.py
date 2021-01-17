import pytest

from material.models import User


@pytest.mark.django_db
def test_user_override_username(organization):
    email = 'foo@example.com'
    user = User.objects.create(email=email, username='foo', organization=organization)
    assert user.username == f'{email}:{organization.id}'


@pytest.mark.django_db
def test_user_superuser_override_username():
    email = 'foo@example.com'
    user = User.objects.create(email=email, username='foo', is_superuser=True)
    assert user.username == email
