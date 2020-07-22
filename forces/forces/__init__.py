"""Fluidattacks Forces package."""
# Standar imports
from contextvars import ContextVar

VERBOSE_LEVEL: ContextVar[int] = ContextVar('verbosity_level', default=3)


def get_verbose_level() -> int:
    """Returns the value of verbose level."""
    return VERBOSE_LEVEL.get()
