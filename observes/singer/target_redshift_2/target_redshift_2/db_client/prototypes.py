# Standard libraries
from typing import (
    Callable,
    cast,
    FrozenSet,
    List,
    Set,
)
# Third party libraries
# Local libraries
from target_redshift_2.db_client.objects import (
    Client,
    ClientPrototype,
    CursorExeAction,
    CursorFetchAction,
    FetchAction,
    IsolatedColumn,
    MutateColumnException,
    PGCURR,
    Table,
    TablePrototype,
)


def client_prototype_1(
    make_exe_action: Callable[[PGCURR, str], CursorExeAction],
    make_fetch_action: Callable[[PGCURR, FetchAction], CursorFetchAction]
) -> ClientPrototype:
    def drop_access_point(self: Client) -> None:
        self.cursor.close()
        self.connection.close()

    def execute(self: Client, statement: str) -> CursorExeAction:
        return make_exe_action(
            self.cursor,
            statement
        )

    def fetchall(self: Client) -> CursorFetchAction:
        return make_fetch_action(
            self.cursor,
            FetchAction.ALL
        )

    def fetchone(self: Client) -> CursorFetchAction:
        return make_fetch_action(
            self.cursor,
            FetchAction.ONE
        )

    return ClientPrototype(
        drop_access_point=drop_access_point,
        execute=execute,
        fetchall=fetchall,
        fetchone=fetchone,
    )


def table_prototype_1(
    make_exe_action: Callable[[str], CursorExeAction]
) -> TablePrototype:

    def table_path(self: Table) -> str:
        return f"\"{self.id.schema.schema_name}\".\"{self.id.table_name}\""

    def add_columns(
        self: Table, new_columns: FrozenSet[IsolatedColumn]
    ) -> List[CursorExeAction]:
        diff_columns: Set[IsolatedColumn] = \
            cast(Set[IsolatedColumn], new_columns) - self.columns
        diff_names: Set[str] = set(map(lambda c: c.name, diff_columns))
        current_names: Set[str] = set(map(lambda c: c.name, self.columns))
        if not diff_names.isdisjoint(current_names):
            raise MutateColumnException(
                'Cannot update the type of existing columns.'
                f'Columns: {diff_names.intersection(current_names)}'
            )
        actions: List[CursorExeAction] = []
        table_path: str = self.table_path()
        for column in diff_columns:
            statement: str = (
                f'ALTER TABLE {table_path} '
                f'ADD COLUMN {column.name} '
                f'{column.field_type} default {column.default_val}'
            )
            actions.append(make_exe_action(statement))
        return actions

    return TablePrototype(
        table_path=table_path,
        add_columns=add_columns
    )
