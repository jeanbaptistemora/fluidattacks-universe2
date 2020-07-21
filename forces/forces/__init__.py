"""Fluidattacks Forces package."""
# Standar imports
from contextvars import ContextVar

INTEGRATES_API_URL: str = 'https://fluidattacks.com/integrates/api'
INTEGRATES_API_TOKEN: ContextVar[str] = ContextVar('integrates_api_token')


def set_api_token(token: str) -> None:
    """Set value for integrates API token."""
    INTEGRATES_API_TOKEN.set(token)


def get_api_token() -> str:
    """Returns the value of integrates API token."""
    return INTEGRATES_API_TOKEN.get()
