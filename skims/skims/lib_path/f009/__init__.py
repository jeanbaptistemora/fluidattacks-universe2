from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    EXTENSIONS_YAML,
    NAMES_DOCKERFILE,
    SHIELD,
)
from lib_path.f009.aws_credentials import (
    aws_credentials,
)
from lib_path.f009.docker_compose_env_secrets import (
    docker_compose_env_secrets,
)
from lib_path.f009.dockerfile_env_secrets import (
    dockerfile_env_secrets,
)
from lib_path.f009.java_properties_sensitive_data import (
    java_properties_sensitive_data,
)
from lib_path.f009.jwt_token import (
    jwt_token,
)
from lib_path.f009.sensitive_key_in_json import (
    sensitive_key_in_json,
)
from lib_path.f009.web_config_db_connection import (
    web_config_db_connection,
)
from lib_path.f009.web_config_user_pass import (
    web_config_user_pass,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
)
from utils.function import (
    TIMEOUT_1MIN,
)


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_aws_credentials(content: str, path: str) -> Vulnerabilities:
    return await in_process(
        aws_credentials,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_dockerfile_env_secrets(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        dockerfile_env_secrets,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_docker_compose_env_secrets(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        docker_compose_env_secrets,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_java_properties_sensitive_data(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        java_properties_sensitive_data,
        content=content,
        path=path,
    )


@SHIELD
@TIMEOUT_1MIN
async def run_sensitive_key_in_json(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        sensitive_key_in_json,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_web_config_user_pass(content: str, path: str) -> Vulnerabilities:
    return await in_process(
        web_config_user_pass,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_web_config_db_connection(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        web_config_db_connection,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_jwt_token(content: str, path: str) -> Vulnerabilities:
    return await in_process(
        jwt_token,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:

    content = content_generator()
    coroutines: List[Awaitable[Vulnerabilities]] = []

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
        coroutines.append(run_aws_credentials(content, path))

    if file_name in NAMES_DOCKERFILE:
        coroutines.append(run_dockerfile_env_secrets(content, path))

    elif file_name == "docker-compose" and file_extension in EXTENSIONS_YAML:
        async for template in load_templates(content, fmt=file_extension):
            coroutines.append(
                run_docker_compose_env_secrets(content, path, template)
            )

    elif file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(run_java_properties_sensitive_data(content, path))

    elif file_extension in {"json"}:
        coroutines.append(run_sensitive_key_in_json(content, path))

    elif file_extension in {"config", "httpsF5", "json", "settings"}:
        coroutines.append(run_web_config_user_pass(content, path))
        coroutines.append(run_web_config_db_connection(content, path))

    return coroutines
