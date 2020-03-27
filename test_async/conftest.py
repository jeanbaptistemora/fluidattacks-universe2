import logging
import pytest
from django.conf import settings

from backend.domain import user as user_domain
from backend import util

logging.config.dictConfig(settings.LOGGING)


@pytest.fixture(autouse=True, scope='session')
def load_enforcers(request):
    """Load policies from DB into the enforcers."""
    user_domain.grant_user_level_role('unittest', 'admin')
    util._temporal_keep_auth_table_fresh(settings.ENFORCER_GROUP_LEVEL_ASYNC)
    util._temporal_keep_auth_table_fresh(settings.ENFORCER_GROUP_LEVEL)
    util._temporal_keep_auth_table_fresh(settings.ENFORCER_USER_LEVEL_ASYNC)
    util._temporal_keep_auth_table_fresh(settings.ENFORCER_USER_LEVEL)


@pytest.fixture(autouse=True)
def disable_logging():
    """Disable logging in all tests."""
    logging.disable(logging.INFO)
