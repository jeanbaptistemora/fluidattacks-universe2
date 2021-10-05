from aioextensions import (
    in_process,
)
from jose.exceptions import (
    JOSEError,
)
from jose.jwt import (
    decode as jwt_decode,
)
from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    get_vulnerabilities_blocking,
    get_vulnerabilities_from_iterator_blocking,
    NAMES_DOCKERFILE,
    SHIELD,
)
from model import (
    core_model,
)
from parse_java_properties import (
    load as load_java_properties,
)
from pyparsing import (
    ParseResults,
    Regex,
)
import re
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Pattern,
    Set,
    Tuple,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from zone import (
    t,
)

# Constants
WS = r"\s*"
WSM = r"\s+"
DOCKERFILE_ENV: Pattern[str] = re.compile(
    fr"^{WS}ENV{WS}(?P<key>[\w\.]+)(?:{WS}={WS}|{WSM})(?P<value>.+?){WS}$",
)


def _validate_jwt(token: str) -> bool:
    try:
        jwt_decode(
            token,
            key="",
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iat": False,
                "verify_exp": False,
                "verify_nbf": False,
                "verify_iss": False,
                "verify_sub": False,
                "verify_jti": False,
                "verify_at_hash": False,
                "leeway": 0,
            },
        )
        return True
    except JOSEError:
        return False


def _aws_credentials(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    grammar = Regex(r"AKIA[A-Z0-9]{16}")

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description=t(
            key="src.lib_path.f009.aws_credentials.description",
            path=path,
        ),
        finding=core_model.FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


def _jwt_token(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    grammar = Regex(
        r"[A-Za-z0-9-_.+\/=]{20,}\."
        r"[A-Za-z0-9-_.+\/=]{20,}\."
        r"[A-Za-z0-9-_.+\/=]{20,}"
    ).addCondition(
        lambda tokens: any(_validate_jwt(token) for token in tokens)
    )

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description=t(
            key="src.lib_path.f009.jwt_token.description",
            path=path,
        ),
        finding=core_model.FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def aws_credentials(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _aws_credentials,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def jwt_token(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _jwt_token,
        content=content,
        path=path,
    )


def _dockerfile_env_secrets(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    secret_smells: Set[str] = {
        "api_key",
        "jboss_pass",
        "license_key",
        "password",
        "secret",
    }

    def iterator() -> Iterator[Tuple[int, int]]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            if match := DOCKERFILE_ENV.match(line):
                secret: str = match.group("key").lower()
                value: str = match.group("value").strip('"').strip("'")
                if (
                    value
                    and not value.startswith("#{")
                    and not value.endswith("}#")
                    and any(smell in secret for smell in secret_smells)
                ):
                    column: int = match.start("value")
                    yield line_no, column

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"798"},
        description=t(
            key="src.lib_path.f009.dockerfile_env_secrets.description",
            path=path,
        ),
        finding=core_model.FindingEnum.F009,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def dockerfile_env_secrets(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _dockerfile_env_secrets,
        content=content,
        path=path,
    )


def _java_properties_sensitive_data(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    sensible_key_smells = {
        "amazon.aws.key",
        "amazon.aws.secret",
        "artifactory_user",
        "artifactory_password",
        "aws.accesskey",
        "aws.secretkey",
        "bg.ws.aws.password",
        "bg.ws.key-store-password",
        "bg.ws.trust-store-password",
        "certificate.password",
        "crypto.password",
        "db.password",
        "database.password",
        "facephi.password",
        "jasypt.encryptor.password",
        "jwt.token.basic.signing.secret",
        "key.alias.password",
        "lambda.credentials2.key",
        "lambda.credentials2.secret",
        "mbda.credentials2.secret",
        "micro.password",
        "org.apache.ws.security.crypto.merlin.alias.password",
        "org.apache.ws.security.crypto.merlin.keystore.password",
        "passwordkeystore",
        "sonar.password",
        "spring.datasource.password",
        "spring.mail.password",
        "spring.mail.username",
        "truststore.password",
        "ws.aws.password",
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

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"798"},
        description=t(
            key="src.lib_path.f009.java_properties_sensitive_data",
            path=path,
        ),
        finding=core_model.FindingEnum.F009,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_properties_sensitive_data(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _java_properties_sensitive_data,
        content=content,
        path=path,
    )


def _sensitive_key_in_json(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    key_smell = {
        "api_key",
        "current_key",
    }

    def check_key(tokens: ParseResults) -> bool:
        for token in tokens:
            key, _ = token.split(":", maxsplit=1)
            if key.strip(' "') in key_smell:
                return True
        return False

    grammar = Regex(r"\s*\"\w+\"\s*:\s*\"[A-Za-z0-9]{5,}\"")
    grammar.addCondition(check_key)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description=t(
            key="src.lib_path.f009.sensitive_key_in_json.description",
            path=path,
        ),
        finding=core_model.FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


@SHIELD
@TIMEOUT_1MIN
async def sensitive_key_in_json(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _sensitive_key_in_json,
        content=content,
        path=path,
    )


def _web_config_user_pass(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    grammar = Regex(r'(username|password)=".+?"', flags=re.IGNORECASE)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description=t(
            key="src.lib_path.f009.web_config_user_pass.description",
            path=path,
        ),
        finding=core_model.FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def web_config_user_pass(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _web_config_user_pass,
        content=content,
        path=path,
    )


def _web_config_db_connection(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    grammar = Regex(r'connectionString=".+?"', flags=re.IGNORECASE)
    grammar.addCondition(
        lambda tokens: any("password" in token.lower() for token in tokens)
    )

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description=t(
            key="src.lib_path.f009.web_config_db_connection.description",
            path=path,
        ),
        finding=core_model.FindingEnum.F009,
        grammar=grammar,
        path=path,
        wrap=True,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def web_config_db_connection(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _web_config_db_connection,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in {
        "groovy",
        "java",
        "jpage",
        "js",
        "json",
        "kt",
        "properties",
        "py",
        "sbt",
        "sql",
        "swift",
        "yaml",
        "yml",
    }:
        coroutines.append(
            aws_credentials(
                content=await content_generator(),
                path=path,
            )
        )
    if file_name in NAMES_DOCKERFILE:
        coroutines.append(
            dockerfile_env_secrets(
                content=await content_generator(),
                path=path,
            )
        )
    elif file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(
            java_properties_sensitive_data(
                content=await content_generator(),
                path=path,
            )
        )
    elif file_extension in {"json"}:
        coroutines.append(
            sensitive_key_in_json(
                content=await content_generator(),
                path=path,
            )
        )
    elif file_extension in {"config", "httpsF5"}:
        content = await content_generator()
        coroutines.append(web_config_user_pass(content=content, path=path))
        coroutines.append(web_config_db_connection(content=content, path=path))

    return coroutines
