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
    template: Any,
) -> Iterator[Any]:
    if isinstance(template, tuple):
        for line in template[0].splitlines():

            if re.search(
                r"Unable to parse stream: No terminal defined for", line
            ):
                yield (0, 0)


def json_unapropiated_comment(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f428.json_unapropiated_elements",
        iterator=_json_line_comments(
            template=template,
        ),
        path=path,
        method=MethodsEnum.JSON_INAPPROPRIATE_ELEMENTS,
    )
