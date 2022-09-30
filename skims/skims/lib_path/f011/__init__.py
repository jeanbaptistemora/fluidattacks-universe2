# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import bs4
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f011.gem import (
    gem_gemfile,
    gem_gemfile_lock,
)
from lib_path.f011.maven import (
    maven_gradle,
    maven_pom_xml,
    maven_sbt,
)
from lib_path.f011.npm import (
    npm_package_json,
    npm_package_lock_json,
    npm_yarn_lock,
)
from lib_path.f011.nuget import (
    nuget_csproj,
    nuget_pkgs_config,
)
from lib_path.f011.pip import (
    pip_requirements_txt,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_gem_gemfile(content: str, path: str) -> Vulnerabilities:
    return gem_gemfile((content, path))


@SHIELD_BLOCKING
def run_gem_gemfile_lock(content: str, path: str) -> Vulnerabilities:
    return gem_gemfile_lock((content, path))


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
def run_npm_package_lock_json(content: str, path: str) -> Vulnerabilities:
    return npm_package_lock_json(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def run_pip_requirements_txt(content: str, path: str) -> Vulnerabilities:
    return pip_requirements_txt(content=content, path=path)


def _is_pom_xml(content: str) -> bool:
    root = bs4.BeautifulSoup(content, features="html.parser")
    if root.project:
        if root.project.get("xmlns"):
            is_pom_xml = (
                str(root.project["xmlns"])
                == "http://maven.apache.org/POM/4.0.0"
            )
            return is_pom_xml
    return False


@SHIELD_BLOCKING
def analyze(  # noqa: MC0001
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    # pylint: disable=too-many-return-statements

    if file_extension == "xml":
        if _is_pom_xml(content_generator()):
            return (run_maven_pom_xml(content_generator(), path),)

    if file_extension == "gradle":
        return (run_maven_gradle(content_generator(), path),)

    if (file_name, file_extension) == ("build", "sbt"):
        return (run_maven_sbt(content_generator(), path),)

    if (file_name, file_extension) == ("yarn", "lock"):
        return (run_npm_yarn_lock(content_generator(), path),)

    if file_extension == "csproj":
        return (run_nuget_csproj(content_generator(), path),)

    if (file_name, file_extension) == ("packages", "config"):
        return (run_nuget_pkgs_config(content_generator(), path),)

    if (file_name, file_extension) == ("package", "json"):
        return (run_npm_package_json(content_generator(), path),)

    if (file_name, file_extension) == ("package-lock", "json"):
        return (run_npm_package_lock_json(content_generator(), path),)

    if (file_name, file_extension) == ("requirements", "txt"):
        return (run_pip_requirements_txt(content_generator(), path),)

    if (file_name, file_extension) == ("Gemfile", "lock"):
        return (run_gem_gemfile_lock(content_generator(), path),)

    if file_name == "Gemfile":
        return (run_gem_gemfile(content_generator(), path),)

    return ()
