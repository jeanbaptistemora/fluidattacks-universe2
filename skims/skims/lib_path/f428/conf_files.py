from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphShardMetadataLanguage as GraphLanguage,
)
from sast.parse import (
    parse_one,
)


def json_invalid_file(
    content: str, path: str, raw_content: bytes
) -> Vulnerabilities:
    method = MethodsEnum.JSON_INAPPROPRIATE_ELEMENTS
    language = GraphLanguage.JSON

    def iterator() -> Iterator[tuple[int, int]]:
        if not parse_one(path, language, raw_content):
            yield (0, 0)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_root.f428.json_unapropiated_elements",
        iterator=iterator(),
        path=path,
        method=method,
    )
