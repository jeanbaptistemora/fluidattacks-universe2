from enum import (
    Enum,
)
from typing import (
    IO,
    NamedTuple,
    Optional,
)

JSONstr = str


class ModuleName(Enum):
    LEADS = "Leads"
    ACCOUNTS = "Accounts"
    CONTACTS = "Contacts"
    DEALS = "Deals"
    CAMPAIGNS = "Campaigns"
    TASKS = "Tasks"
    CASES = "Cases"
    CALLS = "Calls"
    SOLUTIONS = "Solutions"
    PRODUCTS = "Products"
    VENDORS = "Vendors"
    PRICE_BOOKS = "Price_Books"
    QUOTES = "Quotes"
    SALES_ORDERS = "Sales_Orders"
    PURCHASE_ORDERS = "Purchase_Orders"
    INVOICES = "Invoices"


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
    job_id: str
    file: IO[str]
