from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f165.cloudformation import (
    cfn_iam_is_role_over_privileged,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_cfn_iam_is_role_over_privileged(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_is_role_over_privileged(
        content=content, file_ext=file_ext, path=path, template=template
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

    if file_extension in EXTENSIONS_CLOUDFORMATION:

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_iam_is_role_over_privileged(
                    content, file_extension, path, template
                ),
            )

    return results
