from db_model.credentials.types import (
    Credentials,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
import re
from urllib3.util.url import (
    parse_url,
)
from urllib.parse import (
    unquote,
)


def format_git_repo_url(raw_url: str) -> str:
    is_ssh: bool = raw_url.startswith("ssh://") or bool(
        re.match(r"^\w+@.*", raw_url)
    )
    if not is_ssh:
        raw_url = str(parse_url(raw_url)._replace(auth=None))
    url = (
        f"ssh://{raw_url}"
        if is_ssh and not raw_url.startswith("ssh://")
        else raw_url
    )
    return unquote(url).rstrip(" /")


def get_oauth_type(
    credential: Credentials,
) -> str:
    if isinstance(credential.state.secret, OauthGithubSecret):
        return "GITHUB"

    if isinstance(credential.state.secret, OauthGitlabSecret):
        return "GITLAB"

    if isinstance(credential.state.secret, OauthAzureSecret):
        return "AZURE"

    if isinstance(credential.state.secret, OauthBitbucketSecret):
        return "BITBUCKET"

    return ""
