import json
import logging
from ratelimiter import (
    RateLimiter,
)
import requests  # type: ignore
from streamer_zoho_crm.api.bulk.objs import (
    BulkData,
    BulkJob,
    BulkJobResult,
    ModuleName,
)
from streamer_zoho_crm.api.common import (
    API_URL,
    UnexpectedResponse,
)
import tempfile
from typing import (
    Optional,
)
from zipfile import (
    ZipFile,
)

API_ENDPOINT = API_URL + "/crm/bulk/v2/read"
LOG = logging.getLogger(__name__)
rate_limiter = RateLimiter(max_calls=10, period=60)


def create_bulk_read_job(token: str, module: ModuleName, page: int) -> BulkJob:
    with rate_limiter:
        LOG.info("API: Create bulk job for %s @page:%s", module, page)
        endpoint = API_ENDPOINT
        headers = {"Authorization": f"Zoho-oauthtoken {token}"}
        data = {"query": {"module": module.value, "page": page}}
        response = requests.post(url=endpoint, json=data, headers=headers)
        response_json = response.json()
        LOG.debug("response json: %s", str(response_json))
        r_data = response_json["data"][0]["details"]

        return BulkJob(
            operation=r_data["operation"],
            created_by=json.dumps(r_data["created_by"]),
            created_time=json.dumps(r_data["created_time"]),
            state=r_data["state"],
            id=r_data["id"],
            module=module,
            page=page,
            result=None,
        )


def get_bulk_job(token: str, job_id: str) -> BulkJob:
    LOG.info("API: Get bulk job #%s", job_id)
    endpoint = f"{API_ENDPOINT}/{job_id}"
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    response = requests.get(url=endpoint, headers=headers)
    response_json = response.json()
    LOG.debug("response json: %s", str(response_json))
    r_data = response_json["data"][0]
    bulk_result: Optional[BulkJobResult]
    if "result" not in r_data:
        LOG.debug("Result not present")
        bulk_result = None
    else:
        bulk_result = BulkJobResult(
            page=r_data["result"]["page"],
            count_items=r_data["result"]["count"],
            download_url=r_data["result"]["download_url"],
            more_records=r_data["result"]["more_records"],
        )
    return BulkJob(
        operation=r_data["operation"],
        created_by=json.dumps(r_data["created_by"]),
        created_time=r_data["created_time"],
        state=r_data["state"],
        id=r_data["id"],
        module=ModuleName(r_data["query"]["module"]),
        page=r_data["query"]["page"],
        result=bulk_result,
    )


def download_result(token: str, job_id: str) -> BulkData:
    # pylint: disable=consider-using-with
    # need refac of BulkData for enabling the above check
    with rate_limiter:
        LOG.info("API: Download bulk job #%s", job_id)
        endpoint = f"{API_ENDPOINT}/{job_id}/result"
        headers = {"Authorization": f"Zoho-oauthtoken {token}"}
        response = requests.get(url=endpoint, headers=headers)
        tmp_zipdir = tempfile.mkdtemp()
        file_zip = tempfile.NamedTemporaryFile(mode="wb+")
        file_unzip = tempfile.NamedTemporaryFile(mode="w+")
        file_zip.write(response.content)
        file_zip.seek(0)
        LOG.debug("Unzipping file")
        with ZipFile(file_zip, "r") as zip_obj:
            files = zip_obj.namelist()
            if len(files) > 1:
                raise UnexpectedResponse("Zip file with multiple files.")
            zip_obj.extract(files[0], tmp_zipdir)
        LOG.debug("Generating BulkData")
        with open(
            tmp_zipdir + f"/{files[0]}", "r", encoding="UTF-8"
        ) as unzipped:
            file_unzip.write(unzipped.read())
        LOG.debug("Unzipped size: %s", file_unzip.tell())
        return BulkData(job_id=job_id, file=file_unzip)
