from lib_path.common import (
    DependencyType,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)
from parse_json import (
    loads_blocking as json_loads_blocking,
)
from typing import (
    Iterator,
)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.COMPOSER, MethodsEnum.COMPOSER_JSON)
def composer_json(  # NOSONAR
    content: str, path: str
) -> Iterator[DependencyType]:
    content_json = json_loads_blocking(content, default={})
    print(content_json)
    dependencies: Iterator[DependencyType] = (
        (product, version)
        for key in content_json
        if key["item"] == "require"
        for product, version in content_json[key].items()
    )

    return dependencies


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.COMPOSER, MethodsEnum.COMPOSER_LOCK)
def composer_lock(  # NOSONAR
    content: str, path: str
) -> Iterator[DependencyType]:
    content_json = json_loads_blocking(content, default={})
    for key in content_json:
        if key["item"] == "packages":
            for line in content_json[key]["item"]:
                cont = 0
                info = []
                for product in line.values():
                    if cont >= 2:
                        cont = 0
                        break
                    cont += 1
                    info.append(product)
                yield tuple(info)  # type: ignore
