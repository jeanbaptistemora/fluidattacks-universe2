# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from click import (
    argument,
    command,
    option,
)
import sys
from toolbox import (
    resources,
    utils,
)

SUBS_METAVAR = "[GROUP]"


@command(name="resources", short_help="administrate resources")
@argument(
    "group",
    default=utils.generic.get_current_group(),
)
@option(
    "--clone-from-customer-git",
    "clone",
    is_flag=True,
    help="clone the repositories of a group",
)
@option(
    "--name",
    "o_name",
    help="Specific name of repository",
    default="*",
    type=str,
)
@option("--fingerprint", is_flag=True, help="get the fingerprint of a group")
@option("--login", is_flag=True, help="login to AWS through OKTA")
@option(
    "--force",
    is_flag=True,
    help="force clone from customer git",
    default=False,
)
def resources_management(  # pylint: disable=too-many-arguments
    group: str,
    o_name: str,
    clone: bool,
    fingerprint: bool,
    login: bool,
    force: bool = False,
) -> None:
    """Allows administration tasks within groups"""
    success: bool = True

    if clone:
        success = resources.repo_cloning(group, o_name, force=force)
    elif fingerprint:
        success = resources.get_fingerprint(group)
    elif login:
        success = utils.generic.okta_aws_login(f"continuous-{group}")

    sys.exit(0 if success else 1)
