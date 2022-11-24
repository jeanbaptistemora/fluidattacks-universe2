from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from typing import (
    Any,
    Iterator,
)
from utils.function import (
    get_node_by_keys,
)


def _tsconfig_sourcemap_enabled(
    template: Any,
) -> Iterator[Any]:
    if (
        isinstance(template, Node)
        and (
            sourcemap := get_node_by_keys(
                template, ["compilerOptions", "sourceMap"]
            )
        )
        and sourcemap.data is True
    ):
        yield sourcemap.start_line, sourcemap.start_column


def tsconfig_sourcemap_enabled(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f236.tsconfig_sourcemap_enabled",
        iterator=_tsconfig_sourcemap_enabled(
            template=template,
        ),
        path=path,
        method=MethodsEnum.TSCONFIG_SOURCEMAP_ENABLED,
    )
