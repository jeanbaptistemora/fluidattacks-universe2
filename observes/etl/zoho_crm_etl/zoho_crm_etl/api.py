# Standard libraries
import json
from enum import Enum
from typing import (
    Callable,
    NamedTuple,
    Optional,
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
    LEADS = 'Leads'
    ACCOUNTS = 'accounts'
    CONTACTS = 'contacts'
    DEALS = 'deals'
    CAMPAIGNS = 'campaigns'
    TASKS = 'tasks'
    CASES = 'cases'
    MEETINGS = 'meetings'
    CALLS = 'calls'
    SOLUTIONS = 'solutions'
    PRODUCTS = 'Products'
    VENDORS = 'vendors'
    PRICE_BOOKS = 'pricebooks'
    QUOTES = 'quotes'
    SALES_ORDERS = 'salesorders'
    PURCHASE_ORDERS = 'purchaseorders'
    INVOICES = 'invoices'
    CUSTOM = 'custom'


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


rate_limiter = RateLimiter(max_calls=10, period=60)


def create_bulk_read_job(
    token: str, module: ModuleName, page: int
) -> BulkJob:
    with rate_limiter:
        endpoint = f'{API_URL}/crm/bulk/v2/read'
        headers = {'Authorization': f'Zoho-oauthtoken {token}'}
        data = {
            'query': {
                'module': module.value,
                'page': page
            }
        }
        response = requests.post(url=endpoint, json=data, headers=headers)
        r_data = response.json()['data'][0]['details']

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
    endpoint = f'{API_URL}/crm/bulk/v2/read/{job_id}'
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    response = requests.get(url=endpoint, headers=headers)
    r_data = response.json()['data'][0]
    bulk_result: Optional[BulkJobResult]
    if r_data.get('result') is None:
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
