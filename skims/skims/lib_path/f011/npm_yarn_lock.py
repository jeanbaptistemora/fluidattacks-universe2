from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    FindingEnum,
    Platform,
    Vulnerabilities,
)
from more_itertools import (
    windowed,
)
from typing import (
    Iterator,
    Tuple,
)


def npm_yarn_lock(content: str, path: str) -> Vulnerabilities:
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
        finding=FindingEnum.F011,
        path=path,
        platform=Platform.NPM,
    )
