import androguard.core.analysis.analysis
import androguard.core.bytecodes.apk
import bs4
from typing import (
    NamedTuple,
)


class APKContext(NamedTuple):
    analysis: androguard.core.analysis.analysis.Analysis | None
    apk_manifest: bs4.BeautifulSoup | None
    apk_obj: androguard.core.bytecodes.apk.APK | None
    path: str
