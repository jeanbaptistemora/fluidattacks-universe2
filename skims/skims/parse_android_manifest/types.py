# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import androguard.core.analysis.analysis
import androguard.core.bytecodes.apk
import bs4
from typing import (
    NamedTuple,
    Optional,
)


class APKContext(NamedTuple):
    analysis: Optional[androguard.core.analysis.analysis.Analysis]
    apk_manifest: Optional[bs4.BeautifulSoup]
    apk_obj: Optional[androguard.core.bytecodes.apk.APK]
    path: str
