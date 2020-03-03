import logging
import pytest
from django.conf import settings

logging.config.dictConfig(settings.LOGGING)


@pytest.fixture(autouse=True)
def disable_logging():
    """Disable logging in all tests."""
    logging.disable(logging.INFO)
