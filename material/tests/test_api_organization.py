import pytest
from django.urls import reverse

from material.models import User, Organization


def member_list_url(organization):
    return reverse('organization-detail', args=(organization.id,)) + "?expand=users"


@pytest.mark.django_db
def test_organization_detail(api_client, organization):
    response = api_client.get(reverse('organization-detail', args=(organization.id,)))
    assert response.status_code == 200
    expected_result = {
        'id': str(organization.id),
        'lessons': [],
        'name': organization.name,
        'url': f'http://testserver/organizations/{organization.id}/',
    }
    assert response.data == expected_result


@pytest.mark.django_db
def test_organization_member_list_only_if_authenticated(api_client, organization):
    response = api_client.get(member_list_url(organization))
    assert 'users' not in response.data


@pytest.mark.django_db
def test_organization_member_list_only_supervisors_if_not_supervisor(api_client, organization, user, supervisor):
    api_client.force_authenticate(user=user)
    response = api_client.get(member_list_url(organization))
    assert response.status_code == 200
    member_list = response.data['users']
    assert len(member_list) == 1
    assert member_list[0]['id'] == str(supervisor.id)


@pytest.mark.django_db
def test_organization_member_list_all_members_if_supervisor(api_client, organization, user, supervisor):
    api_client.force_authenticate(user=supervisor)
    response = api_client.get(member_list_url(organization))
    assert response.status_code == 200
    member_set = {user['id'] for user in response.data['users']}
    assert member_set == {str(user.id), str(supervisor.id)}


@pytest.mark.django_db
def test_organization_member_list_all_members_if_superuser(api_client, organization, user, supervisor, superuser):
    api_client.force_authenticate(user=superuser)
    response = api_client.get(member_list_url(organization))
    assert response.status_code == 200
    member_set = {user['id'] for user in response.data['users']}
    assert member_set == {str(user.id), str(supervisor.id)}
