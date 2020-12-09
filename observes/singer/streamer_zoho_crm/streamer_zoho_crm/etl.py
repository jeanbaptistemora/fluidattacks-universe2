# Standard libraries
import os
import json
import tempfile
from typing import (
    FrozenSet,
    Iterable,
    Mapping,
    Tuple,
    TypedDict,
)
# Third party libraries
# Local libraries
from postgres_client.connection import ConnectionID
from singer_io import factory
from singer_io.singer import SingerRecord
from streamer_zoho_crm import (
    api,
    bulk,
    db,
    utils,
)
from streamer_zoho_crm.api import (
    ApiClient,
    BulkData,
    BulkJob,
    ModuleName,
)
from streamer_zoho_crm.auth import Credentials
from streamer_zoho_crm.bulk import BulkUtils
from streamer_zoho_crm.db import Client as DbClient


ALL_MODULES = frozenset({ModuleName.CONTACTS})
LOG = utils.get_log(__name__)


class TypeFieldDict(TypedDict):
    field: str
    data_type: str


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


def jobs_map(bulk_utils: BulkUtils) -> Mapping[str, BulkJob]:
    bulk_utils.update_all()
    jobs: FrozenSet[BulkJob] = bulk_utils.get_all()
    id_job_map: FrozenSet[Tuple[str, BulkJob]] = frozenset(
        map(lambda j: (j.id, j), jobs)
    )
    return dict(id_job_map)


def emit_data(
    data: FrozenSet[BulkData],
    id_job_map: Mapping[str, BulkJob],
    module_schema_map: Mapping[str, Iterable[TypeFieldDict]]
) -> None:
    LOG.debug('module schema map: %s', module_schema_map)

    def emit_bulk_data(bdata: BulkData) -> None:
        persistent_file = tempfile.NamedTemporaryFile('w+', delete=False)
        bdata.file.seek(0)
        persistent_file.write(bdata.file.read())
        module_name: str = id_job_map[bdata.job_id].module.value
        module_schema: FrozenSet[Tuple[str, str]] = frozenset(
            map(
                lambda x: (x['field'], x['data_type']),
                module_schema_map.get(module_name, {})
            )
        )
        record = SingerRecord(
            stream=module_name,
            record={
                'csv_path': persistent_file.name,
                'options': {
                    'quote_nonnum': True,
                    'add_default_types': True,
                    'pkeys_present': False,
                    'file_schema': dict(module_schema)
                }
            }
        )
        factory.emit(record)
    list(map(emit_bulk_data, data))


def extraction_phase(
    bulk_utils: BulkUtils,
) -> None:
    id_job_map: Mapping[str, BulkJob] = jobs_map(bulk_utils)
    data: FrozenSet[BulkData] = bulk_utils.extract_data(
        frozenset(id_job_map.keys())
    )
    script_dir = os.path.dirname(__file__)
    schemas_path = 'conf/module_schemas.json'
    with open(os.path.join(script_dir, schemas_path), 'r') as schemas:
        emit_data(data, id_job_map, json.load(schemas))


def start_streamer(
    crm_creds: Credentials,
    db_auth: ConnectionID,
) -> None:
    api_client: ApiClient = api.new_client(crm_creds)
    db_client: DbClient = db.new_client(db_auth)
    bulk_utils: BulkUtils = bulk.new_bulk_utils(api_client, db_client)
    try:
        extraction_phase(bulk_utils)
    finally:
        db_client.close()
