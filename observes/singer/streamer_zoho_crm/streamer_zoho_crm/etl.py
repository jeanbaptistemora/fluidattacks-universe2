# Standard libraries
import logging
import tempfile
from typing import (
    FrozenSet,
    Mapping,
    Tuple,
    TypedDict,
)
# Third party libraries
# Local libraries
from postgres_client.connection import (
    DatabaseID,
    Credentials as DbCredentials,
)
from singer_io import factory
from singer_io.singer import SingerRecord
from streamer_zoho_crm import (
    db,
    api,
)
from streamer_zoho_crm import core
from streamer_zoho_crm.api import (
    ApiClient,
)
from streamer_zoho_crm.api.bulk import (
    BulkData,
    BulkJob,
    ModuleName,
)
from streamer_zoho_crm.api.common import JSON, PageIndex
from streamer_zoho_crm.api.users import UserType, UsersDataPage
from streamer_zoho_crm.auth import Credentials
from streamer_zoho_crm.core import (
    CoreClient,
    IBulk as BulkUtils
)
from streamer_zoho_crm.db import Client as DbClient

ALL_MODULES = frozenset(ModuleName)
LOG = logging.getLogger(__name__)


class TypeFieldDict(TypedDict):
    field: str
    data_type: str


def initialize(
    db_id: DatabaseID,
    db_creds: DbCredentials,
) -> None:
    db.init_db(db_id, db_creds)


def creation_phase(
    crm_creds: Credentials,
    db_id: DatabaseID,
    db_creds: DbCredentials,
    target_modules: FrozenSet[ModuleName] = ALL_MODULES
) -> None:
    """Creates bulk jobs for the `target_modules`"""
    api_client: ApiClient = api.new_client(crm_creds)
    db_client: DbClient = db.new_client(db_id, db_creds)
    core_client: CoreClient = core.new_client(api_client, db_client)
    try:
        bulk_utils: BulkUtils = core_client.bulk
        jobs: FrozenSet[BulkJob] = bulk_utils.get_all()
        banned: FrozenSet[BulkJob] = frozenset(
            filter(lambda x: x.state.upper() != 'COMPLETED', jobs)
        )
        for module in set(target_modules) - banned:
            bulk_utils.create(module, 1)
    finally:
        db_client.close()


def jobs_map(bulk_utils: BulkUtils) -> Mapping[str, BulkJob]:
    bulk_utils.update_all()
    jobs: FrozenSet[BulkJob] = bulk_utils.get_all()
    id_job_map: FrozenSet[Tuple[str, BulkJob]] = frozenset(
        map(lambda j: (j.id, j), jobs)
    )
    return dict(id_job_map)


def emit_bulk_data(
    data: FrozenSet[BulkData],
    id_job_map: Mapping[str, BulkJob],
) -> None:

    def emit(bdata: BulkData) -> None:
        persistent_file = tempfile.NamedTemporaryFile('w+', delete=False)
        bdata.file.seek(0)
        persistent_file.write(bdata.file.read())
        module_name: str = id_job_map[bdata.job_id].module.value
        record = SingerRecord(
            stream=module_name,
            record={
                'csv_path': persistent_file.name,
                'options': {
                    'quote_nonnum': True,
                    'add_default_types': True,
                    'pkeys_present': False,
                    'only_records': True
                }
            }
        )
        factory.emit(record)
    list(map(emit, data))


def emit_user_data(data: UsersDataPage) -> None:
    def emit(user_data: JSON) -> None:
        record = SingerRecord(
            stream='users',
            record=user_data
        )
        factory.emit(record)
    list(map(emit, data.data))


def extraction_phase(
    core_api: CoreClient
) -> None:
    id_job_map: Mapping[str, BulkJob] = jobs_map(core_api.bulk)
    data: FrozenSet[BulkData] = core_api.bulk.extract_data(
        frozenset(id_job_map.keys())
    )
    emit_bulk_data(data, id_job_map)
    users_data = core_api.users.get_users(UserType.ANY, PageIndex(1, 200))
    emit_user_data(users_data)


def start_streamer(
    crm_creds: Credentials,
    db_id: DatabaseID,
    db_creds: DbCredentials
) -> None:
    api_client: ApiClient = api.new_client(crm_creds)
    db_client: DbClient = db.new_client(db_id, db_creds)
    core_client: CoreClient = core.new_client(api_client, db_client)
    try:
        extraction_phase(core_client)
    finally:
        db_client.close()
