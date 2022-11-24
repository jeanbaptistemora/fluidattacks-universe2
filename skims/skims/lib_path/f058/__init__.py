from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f058.android import (
    apk_debugging_enabled,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Tuple,
)


@SHIELD_BLOCKING
def analyze(
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    if (file_name, file_extension) == ("AndroidManifest", "xml"):
        return (apk_debugging_enabled(path),)

    return ()
