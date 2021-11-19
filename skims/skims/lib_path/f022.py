from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from model import (
    core_model,
)
from parse_java_properties import (
    load as load_java_properties,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
)
from utils.function import (
    TIMEOUT_1MIN,
)


def _java_properties_unencrypted_transport(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        data = load_java_properties(
            content,
            include_comments=False,
            exclude_protected_values=True,
        )
        for line_no, (key, val) in data.items():
            val = val.lower()
            if (
                key
                and (val.startswith("http://") or val.startswith("ftp://"))
                and not (
                    "localhost" in val
                    or "127.0.0.1" in val
                    or "0.0.0.0" in val  # nosec
                )
            ):
                yield line_no, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"319"},
        description_key="src.lib_path.f022.unencrypted_channel",
        finding=core_model.FindingEnum.F022,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_properties_unencrypted_transport(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _java_properties_unencrypted_transport,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(
            java_properties_unencrypted_transport(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
