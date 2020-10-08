# Standard library
from typing import (
    Awaitable,
    Callable,
    List,
    Tuple,
)

# Third party libraries
from pyparsing import (
    Keyword,
    MatchFirst,
    nestedExpr,
    Optional,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    C_STYLE_COMMENT,
    SHIELD,
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVA,
    EXTENSIONS_JAVASCRIPT,
    DOUBLE_QUOTED_STRING,
    SINGLE_QUOTED_STRING,
)
from state.cache import (
    CACHE_ETERNALLY,
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


def _csharp_insecure_randoms(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    # secure versions:
    #  - System.Security.Cryptography.RandomNumberGenerator
    #  - System.Security.Cryptography.RNGCryptoServiceProvider
    grammar = (
        Keyword('new') +
        Optional(Keyword('System') + '.') +
        Keyword('Random') +
        nestedExpr()
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(SINGLE_QUOTED_STRING)
    grammar.ignore(DOUBLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'330'},
        description=t(
            key='src.lib_path.f034.csharp_insecure_randoms.description',
            path=path,
        ),
        finding=FindingEnum.F034,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def csharp_insecure_randoms(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _csharp_insecure_randoms,
        content=content,
        path=path,
    )


def _java_use_of_lang_math_random(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    _java = Keyword('java')
    _lang = Keyword('lang')
    _math = Keyword('Math')
    _import = Keyword('import')
    _random = Keyword('random')

    grammar_lang_math_random = MatchFirst([
        # Math.random()
        _math + '.' + _random + nestedExpr(),
        # import java.lang.Math.random
        _import + _java + '.' + _lang + '.' + _math + '.' + _random,
    ])
    grammar_lang_math_random.ignore(C_STYLE_COMMENT)
    grammar_lang_math_random.ignore(SINGLE_QUOTED_STRING)
    grammar_lang_math_random.ignore(DOUBLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'330'},
        description=t(
            key='src.lib_path.f034.java_use_of_lang_math_random.description',
            path=path,
        ),
        finding=FindingEnum.F034,
        grammar=grammar_lang_math_random,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def java_use_of_lang_math_random(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_use_of_lang_math_random,
        content=content,
        path=path,
    )


def _java_use_of_util_random(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    _java = Keyword('java')
    _util = Keyword('util')
    _import = Keyword('import')
    _random = Keyword('Random')
    _args = nestedExpr()

    grammar_util_random = MatchFirst([
        # util.Random()
        _util + '.' + _random + _args,
        # import java.util.Random
        _import + _java + '.' + _util + '.' + _random,
    ])
    grammar_util_random.ignore(C_STYLE_COMMENT)
    grammar_util_random.ignore(SINGLE_QUOTED_STRING)
    grammar_util_random.ignore(DOUBLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'330'},
        description=t(
            key='src.lib_path.f034.java_use_of_util_random.description',
            path=path,
        ),
        finding=FindingEnum.F034,
        grammar=grammar_util_random,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def java_use_of_util_random(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_use_of_util_random,
        content=content,
        path=path,
    )


def _javascript_insecure_randoms(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = Keyword('Math') + '.' + Keyword('random') + nestedExpr()
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(SINGLE_QUOTED_STRING)
    grammar.ignore(DOUBLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'330'},
        description=t(
            key='src.lib_path.f034.javascript_insecure_randoms.description',
            path=path,
        ),
        finding=FindingEnum.F034,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def javascript_insecure_randoms(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _javascript_insecure_randoms,
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

    if file_extension in EXTENSIONS_CSHARP:
        coroutines.append(csharp_insecure_randoms(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_use_of_lang_math_random(
            content=await content_generator(),
            path=path,
        ))
        coroutines.append(java_use_of_util_random(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_insecure_randoms(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
