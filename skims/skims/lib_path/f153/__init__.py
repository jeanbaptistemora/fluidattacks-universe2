from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f153.conf_files import (
    xml_accept_header,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_xml_accept_header(
    content: str,
    path: str,
) -> Vulnerabilities:
    return xml_accept_header(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in ("config", "xml", "jmx"):
        content = content_generator()
        results = (
            *results,
            run_xml_accept_header(content, path),
        )

    return results
