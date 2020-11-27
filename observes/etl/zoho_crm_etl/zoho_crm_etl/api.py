# Standard libraries
import json
import tempfile
from enum import Enum
from typing import (
    Callable,
    IO,
    NamedTuple,
    Optional,
)
from zipfile import ZipFile
# Third party libraries
import requests
from ratelimiter import RateLimiter
# Local libraries
from zoho_crm_etl import auth, utils
from zoho_crm_etl.auth import Credentials


JSONstr = str
API_URL = 'https://www.zohoapis.com'
LOG = utils.get_log(__name__)


class ModuleName(Enum):
    LEADS = 'Leads'
    ACCOUNTS = 'Accounts'
    CONTACTS = 'Contacts'
    DEALS = 'Deals'
    CAMPAIGNS = 'Campaigns'
    TASKS = 'Tasks'
    CASES = 'Cases'
    CALLS = 'Calls'
    SOLUTIONS = 'Solutions'
    PRODUCTS = 'Products'
    VENDORS = 'Vendors'
    PRICE_BOOKS = 'Price_Books'
    QUOTES = 'Quotes'
    SALES_ORDERS = 'Sales_Orders'
    PURCHASE_ORDERS = 'Purchase_Orders'
    INVOICES = 'Invoices'


class BulkJobResult(NamedTuple):
    page: int
    count_items: int
    download_url: str
    more_records: bool


class BulkJob(NamedTuple):
    operation: str
    created_by: JSONstr
    created_time: str
    state: str
    id: str
    module: ModuleName
    page: int
    result: Optional[BulkJobResult] = None


class BulkData(NamedTuple):
    file: IO[str]


class UnexpectedResponse(Exception):
    pass


rate_limiter = RateLimiter(max_calls=10, period=60)


def create_bulk_read_job(
    token: str, module: ModuleName, page: int
) -> BulkJob:
    with rate_limiter:
        LOG.info('API: Create bulk job for %s @page:%s', module, page)
        endpoint = f'{API_URL}/crm/bulk/v2/read'
        headers = {'Authorization': f'Zoho-oauthtoken {token}'}
        data = {
            'query': {
                'module': module.value,
                'page': page
            }
        }
        response = requests.post(url=endpoint, json=data, headers=headers)
        response_json = response.json()
        LOG.debug('response json: %s', str(response_json))
        r_data = response_json['data'][0]['details']

        return BulkJob(
            operation=r_data['operation'],
            created_by=json.dumps(r_data['created_by']),
            created_time=json.dumps(r_data['created_time']),
            state=r_data['state'],
            id=r_data['id'],
            module=module,
            page=page,
            result=None
        )


def get_bulk_job(token: str, job_id: str) -> BulkJob:
    LOG.info('API: Get bulk job #%s', job_id)
    endpoint = f'{API_URL}/crm/bulk/v2/read/{job_id}'
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    response = requests.get(url=endpoint, headers=headers)
    response_json = response.json()
    LOG.debug('response json: %s', str(response_json))
    r_data = response_json['data'][0]
    bulk_result: Optional[BulkJobResult]
    if 'result' not in r_data:
        LOG.debug('Result not present')
        bulk_result = None
    else:
        bulk_result = BulkJobResult(
            page=r_data['result']['page'],
            count_items=r_data['result']['count'],
            download_url=r_data['result']['download_url'],
            more_records=r_data['result']['more_records'],
        )
    return BulkJob(
        operation=r_data['operation'],
        created_by=json.dumps(r_data['created_by']),
        created_time=r_data['created_time'],
        state=r_data['state'],
        id=r_data['id'],
        module=ModuleName(r_data['query']['module']),
        page=r_data['query']['page'],
        result=bulk_result
    )


def download_result(token: str, job_id: str) -> BulkData:
    with rate_limiter:
        LOG.info('API: Download bulk job #%s', job_id)
        endpoint = f'{API_URL}/crm/bulk/v2/read/{job_id}/result'
        headers = {'Authorization': f'Zoho-oauthtoken {token}'}
        response = requests.get(url=endpoint, headers=headers)
        tmp_zipdir = tempfile.mkdtemp()
        file_zip = tempfile.NamedTemporaryFile(mode='wb+')
        file_unzip = tempfile.NamedTemporaryFile(mode='w+')
        file_zip.write(response.content)
        file_zip.seek(0)
        LOG.debug('Unzipping file')
        with ZipFile(file_zip, 'r') as zip_obj:
            files = zip_obj.namelist()
            if len(files) > 1:
                raise UnexpectedResponse('Zip file with multiple files.')
            zip_obj.extract(files[0], tmp_zipdir)
        LOG.debug('Generating BulkData')
        with open(tmp_zipdir + f'/{files[0]}', 'r') as unzipped:
            file_unzip.write(unzipped.read())
        LOG.debug('Unzipped size: %s', file_unzip.tell())
        return BulkData(file=file_unzip)


class ApiClient(NamedTuple):
    create_bulk_read_job: Callable[[ModuleName, int], BulkJob]
    get_bulk_job: Callable[[str], BulkJob]
    download_result: Callable[[str], BulkData]


def new_client(credentials: Credentials) -> ApiClient:
    result = auth.generate_token(credentials)
    token = result['access_token']

    def create_job(module: ModuleName, page: int) -> BulkJob:
        return create_bulk_read_job(token, module, page)

    def get_job(job_id: str) -> BulkJob:
        return get_bulk_job(token, job_id)

    def download_job(job_id: str) -> BulkData:
        return download_result(token, job_id)

    return ApiClient(
        create_bulk_read_job=create_job,
        get_bulk_job=get_job,
        download_result=download_job
    )
