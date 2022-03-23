from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f056.conf_files import (
    json_anon_connection_config,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_json_anon_connection_config(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return json_anon_connection_config(
        content=content, path=path, template=template
    )


def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    content = content_generator()
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in {"json"}:
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_json_anon_connection_config(content, path, template),
            )
    return results
