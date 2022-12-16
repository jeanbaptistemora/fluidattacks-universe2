from .gitlab import (
    GITLAB_ARGS,
)
from authlib.integrations.starlette_client import (
    OAuth,
)

OAUTH = OAuth()
OAUTH.register(**GITLAB_ARGS)

__all__ = ["GITLAB_ARGS", "OAUTH"]
