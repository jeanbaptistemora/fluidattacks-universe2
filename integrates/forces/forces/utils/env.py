import os
from typing import (
    Literal,
)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_ENDPOINT = "https://app.fluidattacks.com/api"
ENDPOINT: str = os.environ.get("API_ENDPOINT", PROD_ENDPOINT)


def guess_environment() -> Literal["development", "production"]:
    return "development" if ENDPOINT != PROD_ENDPOINT else "production"
