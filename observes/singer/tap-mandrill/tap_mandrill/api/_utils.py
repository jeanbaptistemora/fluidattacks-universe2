# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Result,
)
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class ApiError(Exception):
    status_code: str
    text: str

    def __str__(self) -> str:
        return f"status_code={self.status_code} text={self.text}"


def handle_api_error(call: Callable[[], _T]) -> Result[_T, ApiError]:
    try:
        return Result.success(call())
    except ApiClientError as err:  # type: ignore[misc]
        return Result.failure(ApiError(err.status_code, err.text))  # type: ignore[misc]
