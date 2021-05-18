# Standard libraries
from __future__ import annotations
from typing import (
    Iterator,
    NamedTuple,
)

# Third party libraries
# Local libraries
from postgres_client.cursor import act
from postgres_client.client import Client
from . import _queries as queries


class Schema(NamedTuple):
    client: Client
    name: str

    def get_tables(self) -> Iterator[str]:
        actions = queries.get_tables(self.client.cursor, self.name)
        return (item[0] for item in act(actions)[1])

    def exist_on_db(self) -> bool:
        actions = queries.exist_on_db(self.client.cursor, self.name)
        return act(actions)[1][0]

    def delete_on_db(self) -> None:
        action = queries.delete_on_db(self.client.cursor, self.name)
        action.act()

    @classmethod
    def new(cls, client: Client, name: str) -> Schema:
        return cls(client=client, name=name)
