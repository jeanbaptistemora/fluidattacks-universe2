"""Fluid Forces Integrates api package."""
# Standar Library
from contextvars import ContextVar

# Third Library
import jose.jwt

INTEGRATES_API_TOKEN: ContextVar[str] = ContextVar('integrates_api_token')


def set_api_token(token: str) -> None:
    """Set value for integrates API toke"""
    INTEGRATES_API_TOKEN.set(token)


def get_api_token() -> str:
    """Returns the value of integrates API token."""
    return INTEGRATES_API_TOKEN.get()


def get_api_token_email() -> str:
    token = get_api_token()
    result = jose.jwt.get_unverified_claims(token)
    return result['user_email']  # type:ignore


def get_api_token_group() -> str:
    email = get_api_token_email()
    return email.split('@')[0].split('.')[1]
