from ddtrace import (
    patch_all,
)
from ddtrace.runtime import (
    RuntimeMetrics,
)

patch_all(
    aiobotocore=True,
    httplib=True,
    urllib3=True,
)
RuntimeMetrics.enable()
