# Standard libraries
# Third party libraries
# Local libraries
from streamer_zoho_crm.api.bulk import (
    _bulk,
    _objs,
)


ModuleName = _objs.ModuleName
BulkJobResult = _objs.BulkJobResult
BulkJob = _objs.BulkJob
BulkData = _objs.BulkData

create_bulk_read_job = _bulk.create_bulk_read_job
get_bulk_job = _bulk.get_bulk_job
download_result = _bulk.download_result
