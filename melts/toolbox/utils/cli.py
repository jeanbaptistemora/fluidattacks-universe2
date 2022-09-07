# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from click import (
    command,
    echo,
    option,
)
import sys
from toolbox.utils import (
    get_commit_subs,
)


@command(name="utils", short_help="Generic utilities")
@option(
    "--get-commit-subs",
    "o_get_commit_subs",
    help="get the group name from the commmit msg.",
    is_flag=True,
)
def utils_management(
    o_get_commit_subs: bool,
) -> None:
    if o_get_commit_subs:
        subs = get_commit_subs.main()
        echo(subs)
        sys.exit(0 if subs else 1)
