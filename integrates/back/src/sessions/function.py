# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Any,
    Callable,
)


def get_id(function: Callable[..., Any], *extra: Any) -> str:
    """Return a string identifying the provided function.

    The parameter `*extra` will be used as part of the identifier.
    """
    return f"{function.__module__} -> {function.__name__}{extra}"
