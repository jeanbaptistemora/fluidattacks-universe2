# Standard library
import re
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Pattern,
    Tuple,
)

# Third party libraries
from frozendict import (
    frozendict,
)
from more_itertools import (
    windowed,
)

# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from lib_path.common import (
    SHIELD,
)
from model import (
    core_model,
)
from nvd.local import (
    query,
)
from parse_json import (
    loads_blocking as json_loads_blocking,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.ctx import (
    CTX,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from utils.string import (
    to_snippet_blocking,
)
from zone import (
    t,
)

# Constants
DependencyType = Tuple[frozendict, frozendict]

QUOTE = r'["\']'
TEXT = r'[^"\']+'
WS = r"\s*"

# Regexes
RE_MAVEN_A: Pattern[str] = re.compile(
    r"^.*"
    fr"{WS}(?:compile|implementation){WS}[(]?{WS}"
    fr"group{WS}:{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}"
    fr",{WS}name{WS}:{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}"
    fr"(?:,{WS}version{WS}:{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS})?"
    fr".*$"
)
RE_MAVEN_B: Pattern[str] = re.compile(
    r"^.*"
    fr"{WS}(?:compile|implementation){WS}[(]?{WS}"
    fr"{QUOTE}(?P<statement>{TEXT}){QUOTE}"
    fr".*$"
)

# Roadmap:
# | package           | weight | Implemented
# | build.gradle      | 3132   | yes
# | package.json      | 2823   | yes
# | packages.config   | 755    |
# | pom.xml           | 672    |
# | package-lock.json | 555    | yes
# | bower.json        | 158    |
# | yarn.lock         | 47     | yes


def _build_gradle(
    content: str,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            if match := RE_MAVEN_A.match(line):
                column: int = match.start("group")
                product: str = match.group("group") + ":" + match.group("name")
                version: str = match.group("version") or "*"
            elif match := RE_MAVEN_B.match(line):
                column = match.start("statement")
                statement = match.group("statement")
                product, version = (
                    statement.rsplit(":", maxsplit=1)
                    if statement.count(":") >= 2
                    else (statement, "*")
                )
            else:
                continue

            yield (
                {"column": column, "line": line_no, "item": product},
                {"column": column, "line": line_no, "item": version},
            )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=platform,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def build_gradle(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _build_gradle,
        content=content,
        path=path,
        platform=core_model.Platform.MAVEN,
    )


def _npm_package_json(
    content: str,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    content_json = json_loads_blocking(content, default={})

    dependencies: Iterator[DependencyType] = (
        (product, version)
        for key in content_json
        if key["item"] == "dependencies"
        for product, version in content_json[key].items()
    )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        path=path,
        platform=platform,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def npm_package_json(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _npm_package_json,
        content=content,
        path=path,
        platform=core_model.Platform.NPM,
    )


def _npm_package_lock_json(
    content: str,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies(obj: frozendict) -> Iterator[DependencyType]:
        for key in obj:
            if key["item"] in ("dependencies", "devDependencies"):
                for product, spec in obj[key].items():
                    for spec_key, spec_val in spec.items():
                        if spec_key["item"] == "version":
                            yield product, spec_val
                            yield from resolve_dependencies(spec)

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(
            obj=json_loads_blocking(content, default={}),
        ),
        path=path,
        platform=platform,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def npm_package_lock_json(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _npm_package_lock_json,
        content=content,
        path=path,
        platform=core_model.Platform.NPM,
    )


def _yarn_lock(
    content: str,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        windower: Iterator[
            Tuple[Tuple[int, str], Tuple[int, str]],
        ] = windowed(
            fillvalue="",
            n=2,
            seq=tuple(enumerate(content.splitlines(), start=1)),
            step=1,
        )

        # ((11479, 'zen-observable@^0.8.21:'), (11480, '  version "0.8.21"'))
        for (product_line, product), (version_line, version) in windower:
            product, version = product.strip(), version.strip()

            if (
                product.endswith(":")
                and not product.startswith(" ")
                and version.startswith("version")
            ):
                product = product.rstrip(":")
                product = product.split(",", maxsplit=1)[0]
                product = product.strip('"')
                product = product.rsplit("@", maxsplit=1)[0]

                version = version.split(" ", maxsplit=1)[1]
                version = version.strip('"')

                yield (
                    {"column": 0, "line": product_line, "item": product},
                    {"column": 0, "line": version_line, "item": version},
                )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=platform,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def yarn_lock(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _yarn_lock,
        content=content,
        path=path,
        platform=core_model.Platform.NPM,
    )


def translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Iterator[DependencyType],
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    results: core_model.Vulnerabilities = tuple(
        core_model.Vulnerability(
            finding=core_model.FindingEnum.F011,
            kind=core_model.VulnerabilityKindEnum.LINES,
            namespace=CTX.config.namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what=" ".join(
                (
                    path,
                    f'({product["item"]} v{version["item"]})',
                    f"[{cve}]",
                )
            ),
            where=f'{product["line"]}',
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=("937",),
                description=t(
                    key="src.lib_path.f011.npm_package_json.description",
                    path=path,
                    product=product["item"],
                    version=version["item"],
                    cve=cve,
                ),
                snippet=to_snippet_blocking(
                    column=product["column"],
                    content=content,
                    line=product["line"],
                ),
            ),
        )
        for product, version in dependencies
        for cve in query(platform, product["item"], version["item"])
    )

    return results


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if (file_name, file_extension) == ("build", "gradle"):
        coroutines.append(
            build_gradle(
                content=await content_generator(),
                path=path,
            )
        )
    elif (file_name, file_extension) == ("package", "json"):
        coroutines.append(
            npm_package_json(
                content=await content_generator(),
                path=path,
            )
        )
    elif (file_name, file_extension) == ("package-lock", "json"):
        coroutines.append(
            npm_package_lock_json(
                content=await content_generator(),
                path=path,
            )
        )
    elif (file_name, file_extension) == ("yarn", "lock"):
        coroutines.append(
            yarn_lock(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
