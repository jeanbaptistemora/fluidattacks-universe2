# Standard library
from operator import (
    methodcaller,
)
from typing import (
    Awaitable,
    Callable,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from pyparsing import (
    delimitedList,
    Keyword,
    MatchFirst,
    nestedExpr,
)

# Local libraries
from lib_path.common import (
    BACKTICK_QUOTED_STRING,
    get_vulnerabilities_blocking,
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVASCRIPT,
    SHIELD,
    SINGLE_QUOTED_STRING,
    VAR_ATTR_JAVA,
)
from model import (
    core_model,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from zone import (
    t,
)


def _javascript_client_storage(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    conditions: Tuple[Set[str], ...] = (
        # All items in the set must be present to consider it sensitive info
        {'auth'},
        {'credential'},
        {'documento', 'usuario'},
        {'jwt'},
        {'password'},
        {'sesion', 'data'},
        {'sesion', 'id'},
        {'sesion', 'token'},
        {'session', 'data'},
        {'session', 'id'},
        {'session', 'token'},
        {'token', 'access'},
        {'token', 'app'},
        {'token', 'id'},
        {'name', 'user'},
        {'nombre', 'usuario'},
        {'mail', 'user'},
    )

    argument_value = MatchFirst([
        BACKTICK_QUOTED_STRING.copy(),
        DOUBLE_QUOTED_STRING.copy(),
        SINGLE_QUOTED_STRING.copy(),
        VAR_ATTR_JAVA.copy(),
    ])
    arguments = delimitedList(argument_value, delim=',')
    arguments.addCondition(lambda tokens: any(
        all(smell in argument for smell in smells)
        for argument in map(methodcaller('lower'), tokens)
        for smells in conditions
    ))

    grammar = (
        MatchFirst([
            Keyword('localStorage'),
            Keyword('sessionStorage'),
        ]) +
        '.' +
        MatchFirst([
            Keyword('getItem'),
            Keyword('setItem'),
        ]) +
        nestedExpr(
            content=arguments,
            ignoreExpr=None,
        )
    )
    grammar.ignore(C_STYLE_COMMENT)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={'922'},
        description=t(
            key='src.lib_path.f085.client_storage.description',
            path=path,
        ),
        finding=core_model.FindingEnum.F085,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def javascript_client_storage(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _javascript_client_storage,
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

    if file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_client_storage(
            content=await content_generator(),
            path=path,
        ))

    return coroutines
