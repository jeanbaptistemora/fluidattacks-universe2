# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    SHIELD_BLOCKING,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_android_manifest import (
    _apk_exported_cp,
    APKCheckCtx,
    get_apk_context,
    get_check_ctx,
)
from parse_android_manifest.types import (
    APKContext,
)


#  developer: bagudelo@fluidattacks.com
@SHIELD_BLOCKING
def apk_exported_cp(path: str) -> Vulnerabilities:
    apk_ctx: APKContext = get_apk_context(path)
    apk_check_ctx: APKCheckCtx = get_check_ctx(apk_ctx)
    return _apk_exported_cp(ctx=apk_check_ctx)
