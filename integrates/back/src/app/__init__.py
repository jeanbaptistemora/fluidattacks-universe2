from context import (
    CI_COMMIT_SHORT_SHA,
    FI_ENVIRONMENT,
)
from ddtrace import (
    config,
    patch_all,
)
from ddtrace.runtime import (
    RuntimeMetrics,
)

config.env = FI_ENVIRONMENT
config.service = "arm"
config.version = CI_COMMIT_SHORT_SHA
patch_all(
    aiobotocore=True,
    httplib=True,
    urllib3=True,
)
RuntimeMetrics.enable()
