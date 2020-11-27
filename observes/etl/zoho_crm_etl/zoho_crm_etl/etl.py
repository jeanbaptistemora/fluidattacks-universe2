# Standard libraries
from typing import FrozenSet
# Third party libraries
# Local libraries
from postgres_client.connection import ConnectionID
from zoho_crm_etl import (
    api,
    bulk,
    db,
)
from zoho_crm_etl.api import (
    ApiClient,
    BulkJob,
    ModuleName,
)
from zoho_crm_etl.auth import Credentials
from zoho_crm_etl.bulk import BulkUtils
from zoho_crm_etl.db import Client as DbClient


ALL_MODULES = frozenset(ModuleName)


def initialize(db_auth: ConnectionID) -> None:
    db.init_db(db_auth)


def creation_phase(
    crm_creds: Credentials,
    db_auth: ConnectionID,
    target_modules: FrozenSet[ModuleName] = ALL_MODULES
) -> None:
    """Creates bulk jobs for the `target_modules`"""
    api_client: ApiClient = api.new_client(crm_creds)
    db_client: DbClient = db.new_client(db_auth)
    try:
        bulk_utils: BulkUtils = bulk.new_bulk_utils(api_client, db_client)
        jobs: FrozenSet[BulkJob] = bulk_utils.get_all()
        banned: FrozenSet[BulkJob] = frozenset(
            filter(lambda x: x.state.upper() != 'COMPLETED', jobs)
        )
        for module in set(target_modules) - banned:
            bulk_utils.create(module, 1)
    finally:
        db_client.close()
