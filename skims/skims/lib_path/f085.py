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
    resolve,
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
    blocking_get_vulnerabilities,
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVASCRIPT,
    SHIELD,
    SINGLE_QUOTED_STRING,
    VAR_ATTR_JAVA,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _javascript_client_storage(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
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

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f085.client_storage.description',
            path=path,
        ),
        finding=FindingEnum.F085,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def javascript_client_storage(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _javascript_client_storage,
        content=content,
        path=path,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_client_storage(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
