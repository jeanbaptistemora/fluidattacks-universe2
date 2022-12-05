from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import re
from typing import (
    Any,
    Iterator,
)


def _json_line_comments(
    content: str,
) -> Iterator[Any]:
    for line_number, line in enumerate(content.splitlines(), start=1):
        if re.search(r"(([^\S]|^)\/\/.*$)", line):
            yield (line_number, 0)


def json_unapropiated_comment(content: str, path: str) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f428.json_unapropiated_comment",
        iterator=_json_line_comments(
            content=content,
        ),
        path=path,
        method=MethodsEnum.JSON_INAPROPIATE_USE_OF_COMMENTS,
    )
