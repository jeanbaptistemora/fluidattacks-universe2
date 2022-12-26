from .github import (
    GITHUB_ARGS,
)
from .gitlab import (
    GITLAB_ARGS,
)
from authlib.integrations.starlette_client import (
    OAuth,
)

OAUTH = OAuth()
OAUTH.register(**GITLAB_ARGS)
OAUTH.register(**GITHUB_ARGS)

__all__ = ["GITHUB_ARGS", "GITLAB_ARGS", "OAUTH"]
