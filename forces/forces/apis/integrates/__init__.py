"""Fluid Forces Integrates api package."""
# Standar Library
from contextvars import ContextVar

INTEGRATES_API_TOKEN: ContextVar[str] = ContextVar('integrates_api_token')


def set_api_token(token: str) -> None:
    """Set value for integrates API toke"""
    INTEGRATES_API_TOKEN.set(token)


def get_api_token() -> str:
    """Returns the value of integrates API token."""
    return INTEGRATES_API_TOKEN.get()
