# Standard libraries
from typing import NamedTuple


class AzureCredentials(NamedTuple):
    user: str
    password: str
    seed: str
