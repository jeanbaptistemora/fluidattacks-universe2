import asyncio
import logging
import pytest
from django.conf import settings

from backend.domain import user as user_domain

logging.config.dictConfig(settings.LOGGING)


@pytest.fixture(autouse=True, scope='session')
def load_enforcers(request):
    """Load policies from DB into the enforcers."""
    user_domain.grant_user_level_role('unittest', 'admin')


@pytest.fixture(autouse=True)
def disable_logging():
    """Disable logging in all tests."""
    logging.disable(logging.INFO)

