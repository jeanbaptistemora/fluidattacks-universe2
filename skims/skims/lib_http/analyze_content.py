# Standard library
from typing import (
    Callable,
    Dict,
    NamedTuple,
)

# Local libraries
from lib_http.types import (
    URLContext,
)
from model import (
    core_model,
)


class Description(NamedTuple):
    key: str
    kwargs: Dict[str, str]


class ContentCheckCtx(NamedTuple):
    url: URLContext


def get_check_ctx(url: URLContext) -> ContentCheckCtx:
    return ContentCheckCtx(
        url=url,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[ContentCheckCtx], core_model.Vulnerabilities],
] = {}
