from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f428.conf_files import (
    json_invalid_file,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_json_invalid_files(
    content: str,
    path: str,
    raw_content: bytes,
) -> Vulnerabilities:
    return json_invalid_file(
        content=content,
        path=path,
        raw_content=raw_content,
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    raw_content_generator: Callable[[], bytes],
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()
    content = content_generator()
    raw_content = raw_content_generator()
    if file_extension in {"json"}:
        results = (
            *results,
            run_json_invalid_files(content, path, raw_content),
        )

    return results
