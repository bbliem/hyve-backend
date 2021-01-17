import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_section_detail_forbidden(api_client, user, section):
    response = api_client.get(reverse('section-detail', args=(section.id,)))
    assert response.status_code == 401
    # TODO section list?
