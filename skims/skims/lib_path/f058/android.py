from lib_path.common import (
    SHIELD_BLOCKING,
)
from model.core_model import (
    Vulnerabilities,
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


#  developer: bagudelo@fluidattacks.com
@SHIELD_BLOCKING
def apk_debugging_enabled(path: str) -> Vulnerabilities:
    apk_ctx: APKContext = get_apk_context(path)
    apk_check_ctx: APKCheckCtx = get_check_ctx(apk_ctx)
    return _apk_debugging_enabled(ctx=apk_check_ctx)
