from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f428.json import (
    json_unapropiated_comment,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_json_unapropiated_comment(
    content: str,
    path: str,
) -> Vulnerabilities:
    return json_unapropiated_comment(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()
    content = content_generator()
    if file_extension in {"json"}:
        results = (
            *results,
            run_json_unapropiated_comment(content, path),
        )

    return results
