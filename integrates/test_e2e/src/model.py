# Standard libraries
from typing import NamedTuple


class BrowserStackCapacity(NamedTuple):
    os: str
    os_version: str
    browser: str
    browser_version: str
    resolution: str
    name: str


class AzureCredentials(NamedTuple):
    user: str
    password: str
    seed: str
