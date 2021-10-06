import logging
from postgres_client.connection import (
    Credentials as DbCredentials,
    DatabaseID,
)
from singer_io.singer2 import (
    SingerRecord,
)
from singer_io.singer2.emitter import (
    SingerEmitter,
)
from singer_io.singer2.json import (
    JsonEmitter,
    JsonObj,
    JsonValue,
)
from streamer_zoho_crm import (
    api,
    core,
    db,
)
from streamer_zoho_crm.api import (
    ApiClient,
)
from streamer_zoho_crm.api.bulk import (
    BulkData,
    BulkJob,
    ModuleName,
)
from streamer_zoho_crm.api.common import (
    PageIndex,
)
from streamer_zoho_crm.api.users import (
    UsersDataPage,
    UserType,
)
from streamer_zoho_crm.auth import (
    Credentials,
)
from streamer_zoho_crm.core import (
    CoreClient,
    IBulk as BulkUtils,
)
from streamer_zoho_crm.db import (
    Client as DbClient,
)
import tempfile
from typing import (
    FrozenSet,
    Mapping,
    Tuple,
    TypedDict,
)

ALL_MODULES = frozenset(ModuleName)
LOG = logging.getLogger(__name__)
singer_emitter = SingerEmitter(JsonEmitter())


class TypeFieldDict(TypedDict):
    field: str
    data_type: str


class MissingModuleData(Exception):
    pass


def initialize(
    db_id: DatabaseID,
    db_creds: DbCredentials,
) -> None:
    db.init_db(db_id, db_creds)


def creation_phase(
    crm_creds: Credentials,
    db_id: DatabaseID,
    db_creds: DbCredentials,
    target_modules: FrozenSet[ModuleName] = ALL_MODULES,
) -> None:
    """Creates bulk jobs for the `target_modules`"""
    api_client: ApiClient = api.new_client(crm_creds)
    db_client: DbClient = db.new_client(db_id, db_creds)
    core_client: CoreClient = core.new_client(api_client, db_client)
    try:
        bulk_utils: BulkUtils = core_client.bulk
        jobs: FrozenSet[BulkJob] = bulk_utils.get_all()
        triggered_modules: FrozenSet[ModuleName] = frozenset(
            map(lambda x: x.module, jobs)
        )
        bulk_utils.update_all()
        for module in target_modules - triggered_modules:
            bulk_utils.create(module, 1)
    finally:
        db_client.close()


def jobs_map(bulk_utils: BulkUtils) -> Mapping[str, BulkJob]:
    bulk_utils.update_all()
    jobs: FrozenSet[BulkJob] = bulk_utils.get_all()
    id_job_map: FrozenSet[Tuple[str, BulkJob]] = frozenset(
        map(
            lambda j: (j.id, j),
            filter(lambda j: j.state.upper() == "COMPLETED", jobs),
        )
    )
    return dict(id_job_map)


def emit_bulk_data(
    data: FrozenSet[BulkData],
    id_job_map: Mapping[str, BulkJob],
) -> None:
    def emit(bdata: BulkData) -> None:
        with tempfile.NamedTemporaryFile(
            "w+", delete=False
        ) as persistent_file:
            bdata.file.seek(0)
            persistent_file.write(bdata.file.read())
            module_name: str = id_job_map[bdata.job_id].module.value
            record = SingerRecord(
                stream=module_name,
                record={
                    "csv_path": JsonValue(persistent_file.name),
                    "options": JsonValue(
                        {
                            "quote_nonnum": JsonValue(True),
                            "add_default_types": JsonValue(True),
                            "pkeys_present": JsonValue(False),
                            "only_records": JsonValue(True),
                        }
                    ),
                },
            )
            singer_emitter.emit(record)

    list(map(emit, data))


def emit_user_data(data: UsersDataPage) -> None:
    def emit(user_data: JsonObj) -> None:
        record = SingerRecord(stream="users", record=user_data)
        singer_emitter.emit(record)

    list(map(emit, data.data))


def extraction_phase(core_api: CoreClient) -> None:
    id_job_map: Mapping[str, BulkJob] = jobs_map(core_api.bulk)
    ready_modules = frozenset(map(lambda x: x.module, id_job_map.values()))
    missing = ALL_MODULES - ready_modules
    if missing:
        raise MissingModuleData(str(missing))
    data: FrozenSet[BulkData] = core_api.bulk.extract_data(
        frozenset(id_job_map.keys())
    )
    emit_bulk_data(data, id_job_map)
    users_data = core_api.users.get_users(UserType.ANY, PageIndex(1, 200))
    emit_user_data(users_data)


def start_streamer(
    crm_creds: Credentials, db_id: DatabaseID, db_creds: DbCredentials
) -> None:
    api_client: ApiClient = api.new_client(crm_creds)
    db_client: DbClient = db.new_client(db_id, db_creds)
    core_client: CoreClient = core.new_client(api_client, db_client)
    try:
        extraction_phase(core_client)
    finally:
        db_client.close()
