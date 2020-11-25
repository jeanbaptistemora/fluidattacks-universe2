# Standard libraries
import json
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
    Optional,
    TypedDict,
)
# Third party libraries
import requests
from ratelimiter import RateLimiter
# Local libraries
from zoho_crm_etl import auth
from zoho_crm_etl.auth import Credentials


JSONstr = str
API_URL = 'https://www.zohoapis.com'


class ModuleName(Enum):
    LEADS = 'leads'
    ACCOUNTS = 'accounts'
    CONTACTS = 'contacts'
    DEALS = 'deals'
    CAMPAIGNS = 'campaigns'
    TASKS = 'tasks'
    CASES = 'cases'
    MEETINGS = 'meetings'
    CALLS = 'calls'
    SOLUTIONS = 'solutions'
    PRODUCTS = 'products'
    VENDORS = 'vendors'
    PRICE_BOOKS = 'pricebooks'
    QUOTES = 'quotes'
    SALES_ORDERS = 'salesorders'
    PURCHASE_ORDERS = 'purchaseorders'
    INVOICES = 'invoices'
    CUSTOM = 'custom'


class BulkJobResultDict(TypedDict):
    page: int
    count: int
    download_url: str
    more_records: bool


class BulkJobResult(NamedTuple):
    page: int
    count_items: int
    download_url: str
    more_records: bool


def bjob_result_from_json(
    data: BulkJobResultDict
) -> BulkJobResult:
    return BulkJobResult(
        page=data['page'],
        count_items=data['count'],
        download_url=data['download_url'],
        more_records=data['more_records'],
    )


class BulkJobDict(TypedDict):
    operation: str
    created_by: Dict[str, Any]
    created_time: Dict[str, Any]
    state: str
    id: str
    module: ModuleName
    page: int
    result: Optional[BulkJobResultDict]


class BulkJob(NamedTuple):
    operation: str
    created_by: JSONstr
    created_time: JSONstr
    state: str
    id: str
    module: ModuleName
    page: int
    result: Optional[BulkJobResult] = None


def bjob_from_json(
    data: BulkJobDict
) -> BulkJob:
    bjob_result = None
    result = data['result']
    if result:
        bjob_result = bjob_result_from_json(result)
    return BulkJob(
        operation=data['operation'],
        created_by=json.dumps(data['created_by']),
        created_time=json.dumps(data['created_time']),
        state=data['state'],
        id=data['id'],
        module=data['module'],
        page=data['page'],
        result=bjob_result
    )


rate_limiter = RateLimiter(max_calls=10, period=60)


def create_bulk_read_job(
    token: str, module: ModuleName, page: int
) -> BulkJob:
    with rate_limiter:
        endpoint = f'{API_URL}/crm/bulk/v2/read'
        headers = {'Authorization': f'Zoho-oauthtoken {token}'}
        data = {
            'query': {
                'module': module,
                'page': page
            }
        }
        response = requests.post(url=endpoint, data=data, headers=headers)
        r_data = response.json()
        r_data['module'] = module
        r_data['page'] = page
        return bjob_from_json(r_data)


def get_bulk_job(token: str, job_id: str) -> BulkJob:
    endpoint = f'{API_URL}/crm/bulk/v2/read/{job_id}'
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    response = requests.get(url=endpoint, headers=headers)
    data = response.json()
    if data.get('result') is None:
        data['result'] = None
    return bjob_from_json(data)


class ApiClient(NamedTuple):
    create_bulk_read_job: Callable[[ModuleName, int], BulkJob]
    get_bulk_job: Callable[[str], BulkJob]


def new_client(credentials: Credentials) -> ApiClient:
    result = auth.generate_token(credentials)
    token = result['access_token']

    def create_job(module: ModuleName, page: int) -> BulkJob:
        return create_bulk_read_job(token, module, page)

    def get_job(job_id: str) -> BulkJob:
        return get_bulk_job(token, job_id)

    return ApiClient(
        create_bulk_read_job=create_job,
        get_bulk_job=get_job
    )
