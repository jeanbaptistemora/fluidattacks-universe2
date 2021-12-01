from aioextensions import (
    in_process,
)
from lib_path.common import (
    DependencyType,
    SHIELD,
    translate_dependencies_to_vulnerabilities,
)
from model import (
    core_model,
)
from more_itertools import (
    windowed,
)
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
)


def _check_npm_yarn_lock(
    content: str,
    finding: core_model.FindingEnum,
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
        finding=finding,
        path=path,
        platform=platform,
    )


@SHIELD
async def check(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _check_npm_yarn_lock,
        content=content,
        finding=finding,
        path=path,
        platform=core_model.Platform.NPM,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_name: str,
    file_extension: str,
    finding: core_model.FindingEnum,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    if (file_name, file_extension) == ("yarn", "lock"):
        return [
            check(
                content=await content_generator(),
                finding=finding,
                path=path,
            )
        ]

    return []
