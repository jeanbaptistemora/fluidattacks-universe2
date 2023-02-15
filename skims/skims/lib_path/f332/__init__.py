from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_YAML,
    SHIELD_BLOCKING,
)
from lib_path.f332.kubernetes import (
    kubernetes_insecure_port,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
)


@SHIELD_BLOCKING
def run_kubernetes_insecure_port(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return kubernetes_insecure_port(
        content=content, path=path, template=template
    )


def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_YAML:
        content = content_generator()

        results = (
            *results,
            *(
                run_kubernetes_insecure_port(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    return results
