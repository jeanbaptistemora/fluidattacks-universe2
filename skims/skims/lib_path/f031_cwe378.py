from aioextensions import (
    in_process,
)
from lib_path.common import (
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVA,
    get_vulnerabilities_blocking,
    SHIELD,
    SINGLE_QUOTED_STRING,
)
from model import (
    core_model,
)
from pyparsing import (
    Keyword,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    List,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from zone import (
    t,
)


def _java_file_create_temp_file(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    grammar = Keyword("File") + "." + Keyword("createTempFile") + "("
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    translation_key = (
        "src.lib_path.f031_cwe378.java_file_create_temp_file.description"
    )

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"378"},
        description=t(key=translation_key, path=path),
        finding=core_model.FindingEnum.F031_CWE378,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_file_create_temp_file(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _java_file_create_temp_file,
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

    if file_extension in EXTENSIONS_JAVA:
        coroutines.append(
            java_file_create_temp_file(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
