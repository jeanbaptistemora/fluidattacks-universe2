import androguard.core.bytecodes.apk
from typing import (
    NamedTuple,
    Optional,
)


class APKContext(NamedTuple):
    apk_obj: Optional[androguard.core.bytecodes.apk.APK]
    path: str
