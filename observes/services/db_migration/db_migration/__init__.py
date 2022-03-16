from db_migration._patch import (
    Patch,
)
from db_migration.exporter import (
    Exporter,
)
from fa_purity.cmd import (
    Cmd,
)
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from redshift_client.sql_client.connection import (
    connect,
    Credentials,
    DatabaseId,
    IsolationLvl,
)
from redshift_client.sql_client.core import (
    new_client,
)
from redshift_client.table.client import (
    TableClient,
)
from typing import (
    Tuple,
)
from utils_logger.v2 import (
    BugsnagConf,
    set_bugsnag,
    set_main_log,
)

__version__ = "0.1.0"
set_bugsnag(BugsnagConf("service", __version__, __file__, True))
LOG = set_main_log(__name__)


EPHEMERAL_SCHEMAS = frozenset(
    [
        "announcekit",
        "bugsnag",
        "checkly",
        "delighted",
        "formstack",
        "mailchimp",
        "mixpanel_integrates",
        "timedoctor",
    ]
)

TARGETS = frozenset(
    [
        "checkly_old",
        "moodle",
    ]
)


def _schema_filter(schema: SchemaId) -> bool:
    return all(
        [
            not schema.name.startswith("pg_"),
            not schema.name.startswith("dynamodb_"),
            not schema.name.endswith("backup"),
            not schema.name == "information_schema",
            not schema.name in EPHEMERAL_SCHEMAS,
            schema.name in TARGETS,
        ]
    )


def my_exporter(
    old: Tuple[DatabaseId, Credentials], new: Tuple[DatabaseId, Credentials]
) -> Cmd[Exporter]:
    connection_r = connect(old[0], old[1], True, IsolationLvl.AUTOCOMMIT)
    connection_w = connect(new[0], new[1], False, IsolationLvl.AUTOCOMMIT)
    client_r = connection_r.bind(lambda c: new_client(c, LOG))
    client_w = connection_w.bind(lambda c: new_client(c, LOG))
    return client_r.bind(
        lambda r: client_w.map(
            lambda w: Exporter(
                TableClient(r),
                TableClient(w),
                SchemaClient(r),
                SchemaClient(w),
                Patch(_schema_filter),
                "s3://observes.migration",
                "arn:aws:iam::205810638802:role/redshift-role",
            )
        )
    )
