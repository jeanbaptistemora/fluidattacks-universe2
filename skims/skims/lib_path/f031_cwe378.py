# Standard library
from typing import (
    Awaitable,
    Callable,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from pyparsing import (
    Keyword,
)

# Local libraries
from lib_path.common import (
    get_vulnerabilities_blocking,
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVA,
    SHIELD,
    SINGLE_QUOTED_STRING,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _java_file_create_temp_file(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = Keyword('File') + '.' + Keyword('createTempFile') + '('
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    translation_key = (
        'src.lib_path.f031_cwe378.java_file_create_temp_file.description'
    )

    return get_vulnerabilities_blocking(
        content=content,
        cwe={'378'},
        description=t(key=translation_key, path=path),
        finding=FindingEnum.F031_CWE378,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_file_create_temp_file(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
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
) -> List[Awaitable[Tuple[Vulnerability, ...]]]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_file_create_temp_file(
            content=await content_generator(),
            path=path,
        ))

    return coroutines
