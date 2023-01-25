from authlib.integrations.starlette_client import (
    OAuth,
)
from oauth.azure import (
    AZURE_REPOSITORY_ARGS,
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
OAUTH.register(**AZURE_REPOSITORY_ARGS)
OAUTH.register(**BITBUCKET_REPOSITORY_ARGS)
OAUTH.register(**GITLAB_ARGS)
OAUTH.register(**GITHUB_ARGS)


__all__ = [
    "AZURE_REPOSITORY_ARGS",
    "BITBUCKET_REPOSITORY_ARGS",
    "GITHUB_ARGS",
    "GITLAB_ARGS",
    "OAUTH",
]
