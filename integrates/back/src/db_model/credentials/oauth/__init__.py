from authlib.integrations.starlette_client import (
    OAuth,
)
from db_model.credentials.oauth.bitbucket import (
    BITBUCKET_REPOSITORY_ARGS,
)
from db_model.credentials.oauth.github import (
    GITHUB_ARGS,
)
from db_model.credentials.oauth.gitlab import (
    GITLAB_ARGS,
)

OAUTH = OAuth()
OAUTH.register(**BITBUCKET_REPOSITORY_ARGS)
OAUTH.register(**GITLAB_ARGS)
OAUTH.register(**GITHUB_ARGS)

__all__ = ["BITBUCKET_REPOSITORY_ARGS", "GITHUB_ARGS", "GITLAB_ARGS", "OAUTH"]
