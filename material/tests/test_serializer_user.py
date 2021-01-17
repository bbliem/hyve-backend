import pytest

from material.serializers import UserSerializer


@pytest.mark.django_db
def test_user_deserialize(organization):
    email = 'foo@example.com'
    name = 'foo'
    # 1*1 px transparent PNG
    avatar = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=='
    serializer = UserSerializer(data={
        'email': email,
        'organization': str(organization.id),
        'name': name,
        'avatar': avatar,
    })
    assert serializer.is_valid()
    user = serializer.save()
    try:
        assert user.email == email
        assert user.organization == organization
        assert user.username == f'{email}:{str(organization.id)}'
        assert user.name == name
        assert user.avatar.width == 1
        assert user.avatar.height == 1
        assert not user.is_supervisor
        assert not user.is_superuser
    finally:
        # Unfortunately when the transaction is rolled back the uploaded file
        # is not deleted automatically and there doesn't seem to be a hook
        user.avatar.delete()


@pytest.mark.django_db
def test_user_deserialize_ignore_read_only_fields(organization):
    _id = 12345
    email = 'foo@example.com'
    username = 'foo'
    serializer = UserSerializer(data={
        'id': _id,
        'email': email,
        'organization': str(organization.id),
        'username': username,
        'is_supervisor': True,
        'is_superuser': True,
    })
    assert serializer.is_valid()
    user = serializer.save()
    assert user.id != _id
    assert user.username != username
    assert not user.is_supervisor
    assert not user.is_superuser
