from azure.devops.v6_0.git.models import (
    GitRepository,
)
from db_model.azure_repositories.types import (
    BasicRepoData,
)
from typing import (
    Union,
)
from urllib.parse import (
    unquote_plus,
    urlparse,
)


def filter_urls(
    *,
    repository: Union[GitRepository, BasicRepoData],
    urls: set[str],
) -> bool:
    remote_url_filter = (
        unquote_plus(urlparse(repository.remote_url.lower()).path) in urls
    )
    ssh_url_filter = (
        unquote_plus(urlparse(repository.ssh_url.lower()).path) in urls
        or unquote_plus(urlparse(f"ssh://{repository.ssh_url.lower()}").path)
        in urls
    )
    web_url_filter = (
        unquote_plus(urlparse(repository.web_url.lower()).path) in urls
    )

    return not any([remote_url_filter, ssh_url_filter, web_url_filter])
