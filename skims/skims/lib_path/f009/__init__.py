from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    EXTENSIONS_YAML,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f009.aws import (
    aws_credentials,
)
from lib_path.f009.conf_files import (
    jwt_token,
    sensitive_info_in_dotnet_json,
    sensitive_key_in_json,
    web_config_db_connection,
    web_config_user_pass,
)
from lib_path.f009.docker import (
    docker_compose_env_secrets,
    dockerfile_env_secrets,
)
from lib_path.f009.java import (
    java_properties_sensitive_data,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_as_json,
    load_templates_blocking,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_aws_credentials(content: str, path: str) -> Vulnerabilities:
    return aws_credentials(content=content, path=path)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_dockerfile_env_secrets(content: str, path: str) -> Vulnerabilities:
    return dockerfile_env_secrets(content=content, path=path)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_docker_compose_env_secrets(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return docker_compose_env_secrets(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_java_properties_sensitive_data(
    content: str, path: str
) -> Vulnerabilities:
    return java_properties_sensitive_data(content=content, path=path)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_sensitive_key_in_json(content: str, path: str) -> Vulnerabilities:
    return sensitive_key_in_json(content=content, path=path)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_sensitive_info_in_json(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return sensitive_info_in_dotnet_json(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_web_config_user_pass(content: str, path: str) -> Vulnerabilities:
    return web_config_user_pass(content=content, path=path)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_web_config_db_connection(content: str, path: str) -> Vulnerabilities:
    return web_config_db_connection(content=content, path=path)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_jwt_token(content: str, path: str) -> Vulnerabilities:
    return jwt_token(content=content, path=path)


def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    content = content_generator()
    results: Tuple[Vulnerabilities, ...] = ()

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
        results = (*results, run_aws_credentials(content, path))

    if file_name in NAMES_DOCKERFILE:
        results = (*results, run_dockerfile_env_secrets(content, path))

    elif file_name == "docker-compose" and file_extension in EXTENSIONS_YAML:
        results = (
            *results,
            *(
                run_docker_compose_env_secrets(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )

    elif file_extension in EXTENSIONS_JAVA_PROPERTIES:
        results = (*results, run_java_properties_sensitive_data(content, path))

    elif file_extension in {"json"}:
        template = load_as_json(content)
        results = (
            *results,
            run_sensitive_key_in_json(content, path),
            run_sensitive_info_in_json(content, path, template),
        )

    elif file_extension in {"config", "httpsF5", "json", "settings"}:
        results = (
            *results,
            run_web_config_user_pass(content, path),
            run_web_config_db_connection(content, path),
        )

    return results
