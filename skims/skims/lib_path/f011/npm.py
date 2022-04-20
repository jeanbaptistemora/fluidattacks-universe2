from frozendict import (  # type: ignore
    frozendict,
)
from lib_path.common import (
    build_dependencies_tree,
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Platform,
    Vulnerabilities,
)
from more_itertools import (
    windowed,
)
from parse_json import (
    loads_blocking as json_loads_blocking,
)
from typing import (
    Iterator,
    Tuple,
)


def npm_package_json(content: str, path: str) -> Vulnerabilities:
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
        platform=Platform.NPM,
        method=MethodsEnum.NPM_PACKAGE_JSON,
    )


def npm_package_lock_json(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies(
        obj: frozendict, direct_deps: bool = True
    ) -> Iterator[DependencyType]:
        for key in obj:
            if key["item"] == "dependencies":
                for product, spec in obj[key].items():
                    is_dev: bool = False
                    for spec_key, spec_val in spec.items():
                        if spec_key["item"] == "dev":
                            is_dev = spec_val["item"]
                            break

                    should_include: bool = any(
                        [
                            # Analyze direct dependencies
                            # if they are from prod env
                            # they should be included there
                            direct_deps and not is_dev,
                            # Only the prod deps of my deps affect me,
                            # because the dev deps of my deps are not installed
                            not direct_deps and not is_dev,
                        ]
                    )

                    if not should_include:
                        continue

                    for spec_key, spec_val in spec.items():
                        if spec_key["item"] == "version":
                            yield product, spec_val

                    # From this point on, we check the deps of my deps
                    yield from resolve_dependencies(spec, direct_deps=False)

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(
            obj=json_loads_blocking(content, default={}),
        ),
        path=path,
        platform=Platform.NPM,
        method=MethodsEnum.NPM_PACKAGE_LOCK_JSON,
    )


def npm_yarn_lock(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        try:
            json_path = "/".join(path.split("/")[:-1]) + "/package.json"
            dependencies_tree = build_dependencies_tree(
                path_yarn=path,
                path_json=json_path,
                dependencies_type="dependencies",
            )

            for key, value in dependencies_tree.items():
                yield (
                    {
                        "column": 0,
                        "line": value.get("product_line"),
                        "item": key.split("@")[:-1][0],
                    },
                    {
                        "column": 0,
                        "line": value.get("version_line"),
                        "item": value.get("version"),
                    },
                )

        except FileNotFoundError:
            windower: Iterator[
                Tuple[Tuple[int, str], Tuple[int, str]],
            ] = windowed(
                fillvalue="",
                n=2,
                seq=tuple(enumerate(content.splitlines(), start=1)),
                step=1,
            )

            # ((11479, 'zen-observable@^0.8.21:'),
            #  (11480, '  version "0.8.21"'))
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
        platform=Platform.NPM,
        method=MethodsEnum.NPM_YARN_LOCK,
    )
