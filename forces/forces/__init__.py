"""Fluidattacks Forces package."""
# Standar imports
from contextvars import ContextVar

INTEGRATES_API_URL: str = 'https://fluidattacks.com/integrates/api'
INTEGRATES_API_TOKEN: ContextVar[str] = ContextVar('integrates_api_token')
VERBOSE_LEVEL: ContextVar[int] = ContextVar('verbosity_level', default=3)


def set_api_token(token: str) -> None:
    """Set value for integrates API token."""
    INTEGRATES_API_TOKEN.set(token)


def get_api_token() -> str:
    """Returns the value of integrates API token."""
    return INTEGRATES_API_TOKEN.get()


def get_verbose_level() -> int:
    """Returns the value of verbose level."""
    return VERBOSE_LEVEL.get()
