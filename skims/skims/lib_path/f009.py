# Standard library
import re
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Pattern,
    Set,
    Tuple,
)

# Third party libraries
from pyparsing import (
    Keyword,
    MatchFirst,
    nestedExpr,
    Regex,
)
from jose.jwt import decode as jwt_decode
from jose.exceptions import JOSEError

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)

# Local libraries
from lib_path.common import (
    BACKTICK_QUOTED_STRING,
    blocking_get_vulnerabilities,
    blocking_get_vulnerabilities_from_iterator,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVA_PROPERTIES,
    EXTENSIONS_JAVASCRIPT,
    SHIELD,
    NAMES_DOCKERFILE,
    SINGLE_QUOTED_STRING,
)
from parse_java_properties import (
    load as load_java_properties,
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

# Constants
WS = r'\s*'
WSM = r'\s+'
DOCKERFILE_ENV: Pattern[str] = re.compile(
    fr'^{WS}ENV{WS}(?P<key>[\w\.]+)(?:{WS}={WS}|{WSM})(?P<value>.+?){WS}$',
)


def _validate_jwt(token: str) -> bool:
    try:
        jwt_decode(
            token,
            key='',
            options={
                'verify_signature': False,
                'verify_aud': False,
                'verify_iat': False,
                'verify_exp': False,
                'verify_nbf': False,
                'verify_iss': False,
                'verify_sub': False,
                'verify_jti': False,
                'verify_at_hash': False,
                'leeway': 0,
            },
        )
        return True
    except JOSEError:
        return False


def _aws_credentials(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = Regex(r'AKIA[A-Z0-9]{16}')

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'798'},
        description=t(
            key='src.lib_path.f009.aws_credentials.description',
            path=path,
        ),
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


def _jwt_token(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = Regex(
        r'[A-Za-z0-9-_.+\/=]{20,}\.'
        r'[A-Za-z0-9-_.+\/=]{20,}\.'
        r'[A-Za-z0-9-_.+\/=]{20,}').addCondition(
            lambda tokens: any(_validate_jwt(token) for token in tokens))

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'798'},
        description=t(
            key='src.lib_path.f009.jwt_token.description',
            path=path,
        ),
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def aws_credentials(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _aws_credentials,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def jwt_token(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _jwt_token,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def crypto_js_credentials(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
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
            Keyword('Base64'),
            Keyword('Utf16'),
            Keyword('Utf16LE'),
            Keyword('Hex'),
            Keyword('Latin1'),
            Keyword('Utf8'),
        }) + '.' + 'parse' + nestedExpr(
            closer=')',
            content=MatchFirst({
                BACKTICK_QUOTED_STRING.copy(),
                DOUBLE_QUOTED_STRING.copy(),
                SINGLE_QUOTED_STRING.copy(),
            }),
            ignoreExpr=None,
            opener='(',
        )
    )

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'798'},
        description=t(
            key='src.lib_path.f009.crypto_js_credentials.description',
            path=path,
        ),
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


def _dockerfile_env_secrets(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    secret_smells: Set[str] = {
        'api_key',
        'jboss_pass',
        'license_key',
        'password',
        'secret',
    }

    def iterator() -> Iterator[Tuple[int, int]]:
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
                    yield line_no, column

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={'798'},
        description=t(
            key='src.lib_path.f009.dockerfile_env_secrets.description',
            path=path,
        ),
        finding=FindingEnum.F009,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def dockerfile_env_secrets(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _dockerfile_env_secrets,
        content=content,
        path=path,
    )


def _java_properties_sensitive_data(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    sensible_key_smells = {
        'amazon.aws.key',
        'amazon.aws.secret',
        'artifactory_user',
        'artifactory_password',
        'aws.accesskey',
        'aws.secretkey',
        'bg.ws.aws.password',
        'bg.ws.key-store-password',
        'bg.ws.trust-store-password',
        'certificate.password',
        'crypto.password',
        'db.password',
        'database.password',
        'facephi.password',
        'jasypt.encryptor.password',
        'jwt.token.basic.signing.secret',
        'key.alias.password',
        'lambda.credentials2.key',
        'lambda.credentials2.secret',
        'mbda.credentials2.secret',
        'micro.password',
        'org.apache.ws.security.crypto.merlin.alias.password',
        'org.apache.ws.security.crypto.merlin.keystore.password',
        'passwordkeystore',
        'sonar.password',
        'spring.datasource.password',
        'spring.mail.password',
        'spring.mail.username',
        'truststore.password',
        'ws.aws.password',
    }

    def iterator() -> Iterator[Tuple[int, int]]:
        data = load_java_properties(
            content,
            include_comments=True,
            exclude_protected_values=True,
        )
        for line_no, (key, val) in data.items():
            key = key.lower()
            for sensible_key_smell in sensible_key_smells:
                if sensible_key_smell in key and val:
                    yield line_no, 0

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={'798'},
        description=t(
            key='src.lib_path.f009.java_properties_sensitive_data',
            path=path,
        ),
        finding=FindingEnum.F009,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def java_properties_sensitive_data(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_properties_sensitive_data,
        content=content,
        path=path,
    )


@SHIELD
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
        'properties',
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
    elif file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(java_properties_sensitive_data(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
