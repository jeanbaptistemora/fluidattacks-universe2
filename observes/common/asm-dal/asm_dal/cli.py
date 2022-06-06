from .group import (
    GroupsClient,
)
from .organization import (
    OrgsClient,
)
from .utils import (
    AwsCreds,
    new_client,
    new_resource,
    new_session,
)
import click
from fa_purity import (
    Cmd,
    Maybe,
)
import logging
import sys
from typing import (
    NoReturn,
    Optional,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _print(item: _T) -> _T:
    LOG.debug(item)
    return item


@click.command()  # type: ignore[misc]
@click.option("--key-id", type=str, required=True, envvar="AWS_ACCESS_KEY_ID")
@click.option(
    "--secret", type=str, required=True, envvar="AWS_SECRET_ACCESS_KEY"
)
@click.option(
    "--token",
    type=str,
    default=None,
    required=False,
    envvar="AWS_SESSION_TOKEN",
)
def list_all_groups(
    key_id: str, secret: str, token: Optional[str]
) -> NoReturn:
    creds = AwsCreds(
        key_id,
        secret,
        Maybe.from_optional(token),
    )
    session = new_session(creds)
    client = new_client(session)
    resource = new_resource(session)
    orgs_cli = OrgsClient(client)
    grp_cli = GroupsClient(resource)
    groups = (
        orgs_cli.all_orgs()
        .map(lambda o: _print(o))
        .bind(grp_cli.get_groups)
        .map(lambda o: _print(o))
        .to_list()
        .map(lambda l: frozenset(l))
    )
    groups.map(lambda gs: "\n".join(g.name for g in gs)).bind(
        lambda s: Cmd.from_cmd(lambda: print(s, file=sys.stdout))
    ).compute()


@click.group()  # type: ignore[misc]
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(list_all_groups)
