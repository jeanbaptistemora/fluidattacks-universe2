from aioextensions import (
    in_process,
)
import bs4
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from model import (
    core_model,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Set,
    Tuple,
)
from utils.function import (
    TIMEOUT_1MIN,
)


def _has_dangerous_permissions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        dangerous_permissions: Set[str] = {
            "android.permission.ACCEPT_HANDOVER",
            "android.permission.ACCESS_BACKGROUND_LOCATION",
            "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.ACCESS_MEDIA_LOCATION",
            "android.permission.ACTIVITY_RECOGNITION",
            "android.permission.ADD_VOICEMAIL",
            "android.permission.ANSWER_PHONE_CALLS",
            "android.permission.BLUETOOTH_ADVERTISE",
            "android.permission.BLUETOOTH_CONNECT",
            "android.permission.BLUETOOTH_SCAN",
            "android.permission.BODY_SENSORS",
            "android.permission.CALL_PHONE",
            "android.permission.CAMERA",
            "android.permission.GET_ACCOUNTS",
            "android.permission.PROCESS_OUTGOING_CALLS",
            "android.permission.READ_CALENDAR",
            "android.permission.READ_CALL_LOG",
            "android.permission.READ_CONTACTS",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.READ_PHONE_NUMBERS",
            "android.permission.READ_PHONE_STATE",
            "android.permission.READ_SMS",
            "android.permission.RECEIVE_MMS",
            "android.permission.RECEIVE_SMS",
            "android.permission.RECEIVE_WAP_PUSH",
            "android.permission.RECORD_AUDIO",
            "android.permission.SEND_SMS",
            "android.permission.USE_SIP",
            "android.permission.UWB_RANGING",
            "android.permission.WRITE_CALENDAR",
            "android.permission.WRITE_CALL_LOG",
            "android.permission.WRITE_CONTACTS",
            "android.permission.WRITE_EXTERNAL_STORAGE",
        }
        root = bs4.BeautifulSoup(content, features="html.parser")
        for permission in root.find_all("uses-permission", recursive=True):
            if permission["android:name"] in dangerous_permissions:
                line = permission.sourceline
                column = permission.sourcepos
                yield line, column

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"272"},
        description_key="src.lib_path.f346.dangerous_permission",
        finding=core_model.FindingEnum.F346,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def has_dangerous_permissions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _has_dangerous_permissions,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if (file_name, file_extension) == ("AndroidManifest", "xml"):
        coroutines.append(
            has_dangerous_permissions(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
