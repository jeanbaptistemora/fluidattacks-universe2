from click import (
    argument,
    command,
    option,
)
import sys
from toolbox import (
    utils,
)
from toolbox.drills import (
    pull_repos,
    push_repos,
    to_reattack,
    upload_history,
)
from typing import (
    Optional,
)


@command(name="drills", short_help="drills service related tools")
@argument(
    "group",
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group,
)
@option(
    "--name",
    "o_name",
    help="Specific name of repository",
    default=None,
    type=str,
)
@option(
    "--upload-history",
    "o_upload_history",
    is_flag=True,
    help="Show last upload dates on s3 for all groups",
)
@option(
    "--to-reattack",
    "o_to_reattack",
    is_flag=True,
    help="Show findings pending to re-attack and verify",
)
@option(
    "--pull-repos",
    "o_pull_repos",
    is_flag=True,
    help="Pull repos from s3 to fusion for a subs",
)
@option(
    "--push-repos",
    "o_push_repos",
    is_flag=True,
    help="Push repos from fusion to s3 for a subs",
)
@option(
    "--force",
    "o_force",
    is_flag=True,
    help="Push repos from fusion to s3 for a subs",
)
def drills_management(  # pylint: disable=too-many-arguments
    group: str,
    o_name: Optional[str],
    o_upload_history: bool,
    o_to_reattack: bool,
    o_pull_repos: bool,
    o_push_repos: bool,
    o_force: bool,
) -> None:
    """Perform operations with the drills service."""
    success: bool = True

    if o_upload_history:
        upload_history.main()
    elif o_to_reattack:
        group = "all" if group == "unspecified-subs" else group
        to_reattack.main(group)
    elif o_pull_repos:
        success = pull_repos.main(group, o_name)
    elif o_push_repos:
        success = push_repos.main(group, force=o_force)

    sys.exit(0 if success else 1)
