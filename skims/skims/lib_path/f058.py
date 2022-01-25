from lib_path.common import (
    SHIELD_BLOCKING,
)
from model import (
    core_model,
)
from parse_android_manifest import (
    _apk_debugging_enabled,
    APKCheckCtx,
    get_apk_context,
    get_check_ctx,
)
from parse_android_manifest.types import (
    APKContext,
)
from typing import (
    Awaitable,
    List,
)


@SHIELD_BLOCKING
def check(
    path: str,
) -> core_model.Vulnerabilities:
    apk_ctx: APKContext = get_apk_context(path)
    apk_check_ctx: APKCheckCtx = get_check_ctx(apk_ctx)
    return _apk_debugging_enabled(ctx=apk_check_ctx)


@SHIELD_BLOCKING
def analyze(
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    if (file_name, file_extension) == ("AndroidManifest", "xml"):
        return [
            check(
                path=path,
            )
        ]

    return []
