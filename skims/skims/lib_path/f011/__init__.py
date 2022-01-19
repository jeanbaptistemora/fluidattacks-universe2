from aioextensions import (
    in_process,
)
from lib_path.common import (
    SHIELD,
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
from lib_path.f011.npm_package_lock_json import (
    npm_package_lock_json,
)
from lib_path.f011.npm_yarn_lock import (
    npm_yarn_lock,
)
from lib_path.f011.nuget_csproj import (
    nuget_csproj,
)
from lib_path.f011.nuget_packages_config import (
    nuget_packages_config,
)
from model.core_model import (
    FindingEnum,
    Platform,
    Vulnerabilities,
)
from typing import (
    Awaitable,
    Callable,
    List,
)


@SHIELD
async def run_maven_pom_xml(
    content: str, finding: FindingEnum, path: str
) -> Vulnerabilities:
    return await in_process(
        maven_pom_xml,
        content=content,
        finding=finding,
        path=path,
        platform=Platform.MAVEN,
    )


@SHIELD
async def run_maven_gradle(
    content: str, finding: FindingEnum, path: str
) -> Vulnerabilities:
    return await in_process(
        maven_gradle,
        content=content,
        finding=finding,
        path=path,
        platform=Platform.MAVEN,
    )


@SHIELD
async def run_maven_sbt(
    content: str, finding: FindingEnum, path: str
) -> Vulnerabilities:
    return await in_process(
        maven_sbt,
        content=content,
        finding=finding,
        path=path,
        platform=Platform.MAVEN,
    )


@SHIELD
async def run_npm_yarn_lock(
    content: str, finding: FindingEnum, path: str
) -> Vulnerabilities:
    return await in_process(
        npm_yarn_lock,
        content=content,
        finding=finding,
        path=path,
        platform=Platform.NPM,
    )


@SHIELD
async def run_nuget_csproj(
    content: str, finding: FindingEnum, path: str
) -> Vulnerabilities:
    return await in_process(
        nuget_csproj,
        content=content,
        finding=finding,
        path=path,
        platform=Platform.NUGET,
    )


@SHIELD
async def run_nuget_packages_config(
    content: str, finding: FindingEnum, path: str
) -> Vulnerabilities:
    return await in_process(
        nuget_packages_config,
        content=content,
        finding=finding,
        path=path,
        platform=Platform.NUGET,
    )


@SHIELD
async def run_npm_package_json(
    content: str, finding: FindingEnum, path: str
) -> Vulnerabilities:
    return await in_process(
        npm_package_json,
        content=content,
        finding=finding,
        path=path,
        platform=Platform.NPM,
    )


@SHIELD
async def run_npm_package_lock_json(
    content: str, finding: FindingEnum, path: str
) -> Vulnerabilities:
    return await in_process(
        npm_package_lock_json,
        content=content,
        finding=finding,
        path=path,
        platform=Platform.NPM,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    finding: FindingEnum,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    # pylint: disable=too-many-return-statements

    if (file_name, file_extension) == ("pom", "xml"):
        return [run_maven_pom_xml(content_generator(), finding, path)]

    if file_extension == "gradle":
        return [run_maven_gradle(content_generator(), finding, path)]

    if (file_name, file_extension) == ("build", "sbt"):
        return [run_maven_sbt(content_generator(), finding, path)]

    if (file_name, file_extension) == ("yarn", "lock"):
        return [run_npm_yarn_lock(content_generator(), finding, path)]

    if file_extension == "csproj":
        return [run_nuget_csproj(content_generator(), finding, path)]

    if (file_name, file_extension) == ("packages", "config"):
        return [run_nuget_packages_config(content_generator(), finding, path)]

    if (file_name, file_extension) == ("package", "json"):
        return [run_npm_package_json(content_generator(), finding, path)]

    if (file_name, file_extension) == ("package-lock", "json"):
        return [run_npm_package_lock_json(content_generator(), finding, path)]

    return []
