# Standard libraries
from typing import (
    Any,
    Callable,
    Optional,
    NamedTuple,
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
    PGCONN,
    PGCURR,
    SQLidPurifier,
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
    cursor: PGCURR
    sql_id_purifier: SQLidPurifier

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
