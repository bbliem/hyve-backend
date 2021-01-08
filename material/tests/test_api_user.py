import pytest
from django.urls import reverse

from material.models import User


@pytest.mark.django_db
def test_user_list_without_auth(api_client):
    response = api_client.get(reverse('user-list'))
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_list_admin(api_client, admin, user):
    """List all users"""
    api_client.force_authenticate(user=admin)
    response = api_client.get(reverse('user-list'))
    assert response.status_code == 200
    user_ids = {data['id'] for data in response.data}
    assert user_ids == {str(admin.id), str(user.id)}


@pytest.mark.django_db
def test_user_list_unauthorized_user(api_client, user):
    """Only list own user (since Djoser setting HIDE_USERS is not set to False)"""
    # Create another user to check that it isn't listed
    User.objects.create(email='other@example.com', organization=user.organization)
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse('user-list'))
    assert response.status_code == 200
    user_ids = {data['id'] for data in response.data}
    assert user_ids == {str(user.id)}


@pytest.mark.django_db
def test_user_create(api_client, organization):
    data = {
        'email': 'test@example.com',
        'organization': organization.id,
        'password': 'foobarbaz',
    }
    assert User.objects.count() == 0
    response = api_client.post(reverse('user-list'), data, format='json')
    assert response.status_code == 201
    assert User.objects.count() == 1
    for key in ('email', 'organization'):
        assert response.data[key] == data[key]


@pytest.mark.django_db
def test_user_create_without_organization_fails(api_client):
    data = {
        'email': 'test@example.com',
        'password': 'foobarbaz',
    }
    with pytest.raises(TypeError):
        api_client.post(reverse('user-list'), data, format='json')


@pytest.mark.django_db
def test_user_create_with_empty_organization_fails(api_client):
    data = {
        'email': 'test@example.com',
        'password': 'foobarbaz',
        'organization': '',
    }
    response = api_client.post(reverse('user-list'), data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_create_is_superuser_ineffective(api_client, organization):
    data = {
        'email': 'test@example.com',
        'organization': organization.id,
        'password': 'foobarbaz',
        'is_superuser': 'true',
    }
    api_client.post(reverse('user-list'), data, format='json')
    assert User.objects.count() == 1
    assert not User.objects.first().is_superuser


@pytest.mark.django_db
def test_user_detail_unauthorized(api_client, user):
    response = api_client.get(reverse('user-detail', args=(user.id,)))
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_detail(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse('user-detail', args=(user.id,)))
    assert response.status_code == 200
    assert response.data['email'] == user.email
    assert response.data['organization'] == user.organization.id


@pytest.mark.django_db
def test_user_change(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('user-detail', args=(user.id,))
    response = api_client.get(url)
    new_data = response.data
    new_data['email'] = 'newemail@example.com'
    new_data['username'] = f'{new_data["email"]}:{new_data["organization"]}'
    response = api_client.put(url, new_data, format='json')
    assert response.status_code == 200
    response = api_client.get(url)
    assert response.status_code == 200
    for key in new_data:
        assert response.data[key] == new_data[key]

@pytest.mark.django_db
def test_user_change_different_organization_fails(api_client, user):
    # TODO
    assert False


@pytest.mark.django_db
def test_user_change_invalid_username(api_client, user):
    api_client.force_authenticate(user=user)
    # Omit organization from username, which should cause an error
    invalid_username = user.email
    new_data = {
        'username': invalid_username,
        'email': user.email,
        'organization': user.organization.id,
    }
    response = api_client.put(reverse('user-detail', args=(user.id,)), new_data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_change_promotion_to_superuser_fails(api_client, user):
    assert not user.is_superuser
    api_client.force_authenticate(user=user)
    # TODO
    assert False
