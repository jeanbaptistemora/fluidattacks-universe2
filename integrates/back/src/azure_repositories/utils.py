# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from azure.devops.v6_0.git.models import (
    GitRepository,
)


def filter_urls(*, repository: GitRepository, urls: set[str]) -> bool:
    urls = {url.lower() for url in urls}
    remote_url_filter = repository.remote_url.lower() in urls
    ssh_url_filter = (
        repository.ssh_url.lower() in urls
        or f"ssh://{repository.ssh_url}" in urls
    )
    web_url_filter = repository.web_url.lower() in urls

    return not any([remote_url_filter, ssh_url_filter, web_url_filter])
