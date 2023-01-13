from authlib.integrations.starlette_client import (
    OAuth,
)
from oauth.bitbucket import (
    BITBUCKET_REPOSITORY_ARGS,
)
from oauth.github import (
    GITHUB_ARGS,
)
from oauth.gitlab import (
    GITLAB_ARGS,
)

OAUTH = OAuth()
OAUTH.register(**BITBUCKET_REPOSITORY_ARGS)
OAUTH.register(**GITLAB_ARGS)
OAUTH.register(**GITHUB_ARGS)


__all__ = [
    "BITBUCKET_REPOSITORY_ARGS",
    "GITHUB_ARGS",
    "GITLAB_ARGS",
    "OAUTH",
]
