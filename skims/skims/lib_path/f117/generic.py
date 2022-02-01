from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    SHIELD_BLOCKING,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from state.cache import (
    CACHE_ETERNALLY,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def unverifiable_files(path: str, raw_content: bytes) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=raw_content.decode(encoding="utf-8", errors="replace"),
        description_key="src.lib_path.f117.unverifiable_files.description",
        iterator=iter([(1, 0)]),
        path=path,
        method=MethodsEnum.UNVERIFIABLE_FILES,
    )
