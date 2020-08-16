# Standard library
import re
from typing import (
    Awaitable,
    Callable,
    List,
    Pattern,
    Set,
    Tuple,
)

# Third party libraries
from pyparsing import (
    MatchFirst,
    nestedExpr,
    Regex,
)

# Third party libraries
from aioextensions import (
    resolve,
    unblock_cpu,
)

# Local libraries
from lib_path.common import (
    BACKTICK_QUOTED_STRING,
    blocking_get_vulnerabilities,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVASCRIPT,
    HANDLE_ERRORS,
    NAMES_DOCKERFILE,
    SINGLE_QUOTED_STRING,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    to_snippet,
)
from zone import (
    t,
)

# Constants
WS = r'\s*'
WSM = r'\s+'
DOCKERFILE_ENV: Pattern[str] = re.compile(
    fr'^{WS}ENV{WS}(?P<key>[\w\.]+)(?:{WS}={WS}|{WSM})(?P<value>.+?){WS}$',
)


def _aws_credentials(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = Regex(r'AKIA[A-Z0-9]{16}')

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f009.aws_credentials.description',
            path=path,
        ),
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@HANDLE_ERRORS
async def aws_credentials(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _aws_credentials,
        content=content,
        path=path,
    )


@cache_decorator()
@HANDLE_ERRORS
async def crypto_js_credentials(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _crypto_js_credentials,
        content=content,
        path=path,
    )


def _crypto_js_credentials(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = (
        'CryptoJS' + '.' + 'enc' + '.' + MatchFirst({
            'Base64',
            'Utf16',
            'Utf16LE',
            'Hex',
            'Latin1',
            'Utf8',
        }) + '.' + 'parse' + nestedExpr(
            closer=')',
            content=MatchFirst({
                BACKTICK_QUOTED_STRING,
                DOUBLE_QUOTED_STRING,
                SINGLE_QUOTED_STRING,
            }),
            ignoreExpr=None,
            opener='(',
        )
    )

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f009.crypto_js_credentials.description',
            path=path,
        ),
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


def _dockerfile_env_secrets(content: str) -> Tuple[Tuple[int, int], ...]:
    secret_smells: Set[str] = {
        'api_key',
        'jboss_pass',
        'license_key',
        'password',
        'secret',
    }

    secrets: List[Tuple[int, int]] = []
    for line_no, line in enumerate(content.splitlines(), start=1):
        if match := DOCKERFILE_ENV.match(line):
            secret: str = match.group('key').lower()
            value: str = match.group('value').strip('"').strip("'")
            if (
                value
                and not value.startswith('#{') and not value.endswith('}#')
                and any(smell in secret for smell in secret_smells)
            ):
                column: int = match.start('value')
                secrets.append((line_no, column))

    return tuple(secrets)


@cache_decorator()
async def dockerfile_env_secrets(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return tuple([
        Vulnerability(
            finding=FindingEnum.F011,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{line_no}',
            skims_metadata=SkimsVulnerabilityMetadata(
                description=t(
                    key='src.lib_path.f009.dockerfile_env_secrets.description',
                    path=path,
                ),
                snippet=await to_snippet(
                    column=column,
                    content=content,
                    line=line_no,
                )
            )
        )
        for line_no, column in await unblock_cpu(
            _dockerfile_env_secrets, content,
        )
    ])


async def analyze(  # pylint: disable=too-many-arguments
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    file_name: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in {
        'groovy',
        'java',
        'jpage',
        'js',
        'json',
        'py',
        'sbt',
        'sql',
        'swift',
        'yaml',
        'yml',
    }:
        coroutines.append(aws_credentials(
            content=await content_generator(),
            path=path,
        ))

    if file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(crypto_js_credentials(
            content=await content_generator(),
            path=path,
        ))
    elif file_name in NAMES_DOCKERFILE:
        coroutines.append(dockerfile_env_secrets(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
