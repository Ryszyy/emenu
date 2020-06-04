import pytest
from django.contrib.auth import get_user_model

from emenu.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> get_user_model():  # type: ignore
    return UserFactory()
