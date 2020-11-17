from typing import (
    Any,
    Callable,
    cast,
    List,
    Optional,
    NamedTuple,
    Tuple,
)
# Third party libraries
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
from psycopg2 import sql as postgres_sql

# Local libraries
from target_redshift_2.db_client.objects import (
    Client,
    ClientPrototype,
    ConnectionID,
    CursorExeAction,
    CursorFetchAction, DynamicSQLargs,
    FetchAction,
    IsolatedColumn,
    PGCONN,
    PGCURR,
    SQLidPurifier,
    Table,
    TableCreationFail,
    TableID,
    TablePrototype,
)
from target_redshift_2.db_client import prototypes
from target_redshift_2.utils import log


class SQLidPurifierFactory(NamedTuple):
    """Generator of `CursorAction` objects"""
    sql_lib: Any = postgres_sql

    def sql_id_purifier(self: 'SQLidPurifierFactory') -> SQLidPurifier:
        return prototypes.sql_id_purifier_1(self.sql_lib)


class CursorActionFactory(NamedTuple):
    """Generator of `CursorAction` objects"""
    # pylint: disable=too-many-function-args
    # required due to a bug with callable properties
    cursor: PGCURR
    sql_id_purifier: SQLidPurifier = SQLidPurifierFactory().sql_id_purifier()

    def exe_action(
        self: 'CursorActionFactory',
        statement: str,
        args: Optional[DynamicSQLargs] = None
    ) -> CursorExeAction:
        """Generator of `CursorExeAction` objects"""
        def action() -> Any:
            try:
                safe_stm = self.sql_id_purifier(statement, args)
                stm_values = args.values if args else {}
                self.cursor.execute(safe_stm, stm_values)
            except postgres.ProgrammingError as exc:
                log('EXCEPTION', f'{type(exc)} {exc}')
                raise exc
        return CursorExeAction(
            cursor=self.cursor,
            statement=statement,
            act=action
        )

    def fetch_action(
        self: 'CursorActionFactory', f_action: FetchAction
    ) -> CursorFetchAction:
        """Generator of `CursorFetchAction` objects"""
        def action() -> Any:
            try:
                if f_action == FetchAction.ALL:
                    return self.cursor.fetchall()
                return self.cursor.fetchone()
            except postgres.ProgrammingError as exc:
                log('EXCEPTION', f'{type(exc)} {exc}')
                raise exc
        return CursorFetchAction(
            cursor=self.cursor,
            act=action,
            fetch_type=f_action
        )


class ClientFactory(NamedTuple):
    """Generator of `Client` objects"""
    db_connect: Callable[..., PGCONN] = postgres.connect
    isolation_lvl: Any = postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT

    def make_access_point(self: 'ClientFactory', auth: ConnectionID) -> Client:
        dbcon: PGCONN = self.db_connect(
            dbname=auth.dbname,
            user=auth.user,
            password=auth.password,
            host=auth.host,
            port=auth.port
        )
        dbcon.set_session(readonly=False)
        dbcon.set_isolation_level(self.isolation_lvl)
        dbcur: PGCURR = dbcon.cursor()
        purifier_factory = SQLidPurifierFactory()
        purifier = purifier_factory.sql_id_purifier()

        def make_exe_action(
            client: Client, statement: str, args: Optional[DynamicSQLargs]
        ) -> CursorExeAction:
            action_factory: CursorActionFactory = CursorActionFactory(
                client.cursor, purifier
            )
            return action_factory.exe_action(statement, args)

        def make_fetch_action(
            client: Client, f_action: FetchAction
        ) -> CursorFetchAction:
            action_factory: CursorActionFactory = CursorActionFactory(
                client.cursor, purifier
            )
            return action_factory.fetch_action(f_action)

        prototype: ClientPrototype = prototypes.client_prototype_1(
            make_exe_action=make_exe_action,
            make_fetch_action=make_fetch_action,
        )
        return Client(
            connection=dbcon, cursor=dbcur, prototype=prototype
        )


class TableFactory(NamedTuple):
    """Generator of `Table` objects"""
    db_client: Client
    c_action_factory: 'CursorActionFactory'

    def exist(self: 'TableFactory', table_id: TableID) -> bool:
        """Check existence of a Table on the DB"""
        statement = """
            SELECT EXISTS (
                SELECT * FROM information_schema.tables
                WHERE table_schema = %(table_schema)s
                AND table_name = %(table_name)s
            );
        """
        action = self.db_client.execute(
            statement,
            DynamicSQLargs(
                values={
                    'table_schema': table_id.schema.schema_name,
                    'table_name': table_id.table_name
                }
            )
        )
        action.act()
        result: Tuple[bool] = self.db_client.cursor.fetchone()
        return result[0]

    def retrieve(self: 'TableFactory', table_id: TableID) -> Optional[Table]:
        """Retrieve Table from DB"""
        statement = """
            SELECT ordinal_position AS position,
                column_name,
                data_type,
                CASE WHEN character_maximum_length IS not null
                        THEN character_maximum_length
                        ELSE numeric_precision end AS max_length,
                is_nullable,
                column_default AS default_value
            FROM information_schema.columns
            WHERE table_name = %(table_name)s
              AND table_schema = %(table_schema)s
            ORDER BY ordinal_position;
        """
        action: CursorExeAction = self.db_client.execute(
            statement,
            DynamicSQLargs(
                values={
                    'table_schema': table_id.schema.schema_name,
                    'table_name': table_id.table_name
                }
            )
        )
        fetch_action: CursorFetchAction = self.db_client.fetchall()

        action.act()
        results: List[Tuple[Any, ...]] = cast(
            List[Tuple[Any, ...]], fetch_action.act()
        )
        columns = set()
        for column in results:
            columns.add(IsolatedColumn(column[1], column[2], column[5]))

        prototype: TablePrototype = prototypes.table_prototype_1(
            make_exe_action=self.c_action_factory.exe_action
        )
        return Table(
            table_id,
            primary_keys=frozenset(),
            columns=frozenset(columns),
            prototype=prototype
        )

    def create(
        self: 'TableFactory',
        table_draft: Table,
        if_not_exist: bool = False
    ) -> Table:
        """Creates a Table in the DB and returns it"""
        table_path: str = table_draft.table_path()
        pkeys_fields: str = ''
        if table_draft.primary_keys:
            p_fields: str = ",".join(
                [f"{{pkey_{n}}}" for n in range(len(table_draft.primary_keys))]
            )
            pkeys_fields = f',PRIMARY KEY({p_fields})'
        not_exists: str = '' if not if_not_exist else 'IF NOT EXISTS '
        fields: str = ",".join(
            [
                f"{{name_{n}}} {{field_type_{n}}}"
                for n in range(len(table_draft.columns))
            ]
        )
        fields_def: str = f'{fields}{pkeys_fields}'
        statement: str = (
            f"CREATE TABLE {not_exists}{{table_path}} ({fields_def})"
        )
        identifiers = {
            'table_path': table_path
        }
        for index, value in enumerate(table_draft.primary_keys):
            identifiers[f'pkey_{index}'] = value
        for index, column in enumerate(table_draft.columns):
            identifiers[f'name_{index}'] = column.name
            identifiers[f'field_type_{index}'] = column.field_type

        self.db_client.execute(
            statement,
            DynamicSQLargs(
                identifiers=identifiers
            )
        )
        result: Optional[Table] = self.retrieve(table_draft.id)
        if result:
            return result
        raise TableCreationFail(
            'Could not create and verify the existence of table: '
            f'{table_draft.id}'
        )
