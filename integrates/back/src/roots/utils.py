# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
