from lib_path.common import (
    DependencyType,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)
from typing import (
    Iterator,
)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.COMPOSER, MethodsEnum.COMPOSER_JSON)
def composer_json(  # NOSONAR
    content: str, path: str
) -> Iterator[DependencyType]:
    return iter([({}, {})])
