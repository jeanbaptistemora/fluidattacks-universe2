from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f428.json import (
    json_unapropiated_comment,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_comments,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_json_unapropiated_comment(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return json_unapropiated_comment(
        content=content,
        path=path,
        template=template,
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
        for template in load_templates_comments(content, fmt=file_extension):
            results = (
                *results,
                run_json_unapropiated_comment(content, path, template),
            )

    return results
