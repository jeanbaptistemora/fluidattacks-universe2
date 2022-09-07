# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .group import (
    GroupsClient,
)
from .organization import (
    OrgsClient,
)
from .utils import (
    new_client,
    new_resource,
    new_session,
)
import click
from fa_purity import (
    Cmd,
)
import logging
import sys
from typing import (
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _print(item: _T) -> _T:
    LOG.debug(item)
    return item


@click.command(help="Requires AWS authentication (retrieved from the environment)")  # type: ignore[misc]
def list_all_groups() -> NoReturn:
    clients = new_session().bind(
        lambda s: new_client(s)
        .map(OrgsClient)
        .bind(
            lambda o: new_resource(s).map(GroupsClient).map(lambda g: (o, g))
        )
    )

    def _action(orgs_cli: OrgsClient, grp_cli: GroupsClient) -> Cmd[None]:
        groups = (
            orgs_cli.all_orgs()
            .map(lambda o: _print(o))
            .bind(grp_cli.get_groups)
            .map(lambda o: _print(o))
            .to_list()
            .map(lambda l: frozenset(l))
        )
        return groups.map(lambda gs: "\n".join(g.name for g in gs)).bind(
            lambda s: Cmd.from_cmd(lambda: print(s, file=sys.stdout))
        )

    cmd: Cmd[None] = clients.bind(lambda t: _action(t[0], t[1]))
    cmd.compute()


@click.group()  # type: ignore[misc]
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(list_all_groups)
