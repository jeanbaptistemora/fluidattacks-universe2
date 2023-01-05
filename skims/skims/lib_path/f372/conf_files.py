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


def _json_https_flag_missing(
    template: Any,
) -> Iterator[Any]:
    required_flags = {" -S", " --tls", " --ssl"}
    if (
        isinstance(template, Node)
        and (hasattr(template.inner, "get"))
        and (scripts := getattr(template.inner.get("scripts"), "data", None))
        and (hasattr(scripts, "values"))
    ):
        for script in scripts.values():
            if "http-server" in script.data and not any(
                flag in script.data for flag in required_flags
            ):
                yield script.start_line, script.start_column


def json_https_flag_missing(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f372.json_https_flag_missing",
        iterator=_json_https_flag_missing(
            template=template,
        ),
        path=path,
        method=MethodsEnum.JSON_HTTPS_FLAG_MISSING,
    )
