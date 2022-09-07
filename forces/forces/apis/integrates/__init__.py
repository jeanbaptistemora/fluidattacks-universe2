# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""Fluid Forces Integrates api package."""

from contextvars import (
    ContextVar,
)

INTEGRATES_API_TOKEN: ContextVar[str] = ContextVar("integrates_api_token")


def set_api_token(token: str) -> None:
    """Set value for integrates API toke"""
    INTEGRATES_API_TOKEN.set(token)


def get_api_token() -> str:
    """Returns the value of integrates API token."""
    return INTEGRATES_API_TOKEN.get()
