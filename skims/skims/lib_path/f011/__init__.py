from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f011.maven_gradle import (
    maven_gradle,
)
from lib_path.f011.maven_pom_xml import (
    maven_pom_xml,
)
from lib_path.f011.maven_sbt import (
    maven_sbt,
)
from lib_path.f011.npm_package_json import (
    npm_package_json,
)
from lib_path.f011.npm_pkg_lock_json import (
    npm_pkg_lock_json,
)
from lib_path.f011.npm_yarn_lock import (
    npm_yarn_lock,
)
from lib_path.f011.nuget_csproj import (
    nuget_csproj,
)
from lib_path.f011.nuget_pkgs_config import (
    nuget_pkgs_config,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    List,
)


@SHIELD_BLOCKING
def run_maven_pom_xml(content: str, path: str) -> Vulnerabilities:
    return maven_pom_xml(content=content, path=path)


@SHIELD_BLOCKING
def run_maven_gradle(content: str, path: str) -> Vulnerabilities:
    return maven_gradle(content=content, path=path)


@SHIELD_BLOCKING
def run_maven_sbt(content: str, path: str) -> Vulnerabilities:
    return maven_sbt(content=content, path=path)


@SHIELD_BLOCKING
def run_npm_yarn_lock(content: str, path: str) -> Vulnerabilities:
    return npm_yarn_lock(content=content, path=path)


@SHIELD_BLOCKING
def run_nuget_csproj(content: str, path: str) -> Vulnerabilities:
    return nuget_csproj(content=content, path=path)


@SHIELD_BLOCKING
def run_nuget_pkgs_config(content: str, path: str) -> Vulnerabilities:
    return nuget_pkgs_config(content=content, path=path)


@SHIELD_BLOCKING
def run_npm_package_json(content: str, path: str) -> Vulnerabilities:
    return npm_package_json(content=content, path=path)


@SHIELD_BLOCKING
def run_npm_pkg_lock_json(content: str, path: str) -> Vulnerabilities:
    return npm_pkg_lock_json(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> List[Vulnerabilities]:
    # pylint: disable=too-many-return-statements

    if (file_name, file_extension) == ("pom", "xml"):
        return [run_maven_pom_xml(content_generator(), path)]

    if file_extension == "gradle":
        return [run_maven_gradle(content_generator(), path)]

    if (file_name, file_extension) == ("build", "sbt"):
        return [run_maven_sbt(content_generator(), path)]

    if (file_name, file_extension) == ("yarn", "lock"):
        return [run_npm_yarn_lock(content_generator(), path)]

    if file_extension == "csproj":
        return [run_nuget_csproj(content_generator(), path)]

    if (file_name, file_extension) == ("packages", "config"):
        return [run_nuget_pkgs_config(content_generator(), path)]

    if (file_name, file_extension) == ("package", "json"):
        return [run_npm_package_json(content_generator(), path)]

    if (file_name, file_extension) == ("package-lock", "json"):
        return [run_npm_pkg_lock_json(content_generator(), path)]

    return []
