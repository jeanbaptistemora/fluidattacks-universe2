"""Singer tap for the Matomo API."""

import argparse
from concurrent.futures import (
    ThreadPoolExecutor,
)
import copy
from datetime import (
    datetime,
    timedelta,
)
import functools
import os
import re
import requests
from tap_matomo import (
    logs,
)
from tap_matomo.constants import (
    REFERRER_TYPES,
    TABLE_LIST,
    WEBSITE_IDS,
)
import time
from typing import (
    Any,
    Callable,
    Tuple,
)
import uuid

# Type aliases that improve clarity
JSON = Any

# URL to the Matomo API
API_URL = "https://fluidattacks.matomo.cloud"

API_TOKEN = os.environ["MATOMO_API_TOKEN"]


def retry_on_errors(func: Callable) -> Callable:
    """Decorate function to retry if an error occurs."""

    @functools.wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        """Retry the function if status code is not 200
        or response is erroneous."""
        for _ in range(3):
            try:
                (status_code, response) = func(*args, **kwargs)
            except requests.exceptions.ConnectionError as error:
                logs.log_error(f"INFO: {error}")
                logs.log_error("INFO: Retrying...")
                time.sleep(3.0)
                continue

            if status_code != 200:
                logs.log_error(f"INFO: Code {status_code} error - Retrying...")
                time.sleep(3.0)
                continue

            result = ""
            if isinstance(response, dict):
                result = response.get("result", "")
            if result.lower() == "error":
                logs.log_error("INFO: API error - Retrying...")
                time.sleep(3.0)
            else:
                break
        return (status_code, response)

    return decorated


@retry_on_errors
def get_request_response(resource: str) -> Tuple[int, Any]:
    """Make a request for a resource."""

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.get(resource, headers=headers, timeout=60)

    return (response.status_code, response.json())


def get_matomo_data(method: str, site: str, date: str) -> JSON:
    """Get Matomo data for a specific method and website."""

    resource = f"{API_URL}/?module=API&method={method}"
    resource += f"&idSite={site}&period=day&date={date}&format=JSON"
    resource += "&filter_limit=-1"
    resource += f"&token_auth={API_TOKEN}"
    json_objs = get_request_response(resource)[1]

    if method == "VisitsSummary.get":
        json_objs["date"] = date
        return [json_objs]

    for obj in json_objs:
        obj["date"] = date

    return json_objs


def write_records(schema: JSON, method: str, end_date_str: str) -> None:
    """Write the records for this table."""

    record: JSON = {
        "type": "RECORD",
        "stream": schema["stream"],
        "record": schema["schema"]["properties"],
    }

    # Period from the day Matomo started collecting data to current date
    start_date = datetime(2021, 9, 1)
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    dates = [
        start_date + timedelta(days=x)
        for x in range((end_date - start_date).days)
    ]
    dates_str = [datetime.strftime(date, "%Y-%m-%d") for date in dates]

    for site in ["1", "2", "3"]:
        record["record"]["website"] = WEBSITE_IDS[site]
        responses = []

        with ThreadPoolExecutor(max_workers=8) as executor:
            for response in executor.map(
                get_matomo_data,
                [method] * len(dates),
                [site] * len(dates),
                dates_str,
            ):
                responses.extend(response)

        for response in responses:
            record["record"]["uuid"] = str(uuid.uuid4())
            for key in record["record"].keys():
                if key in ["uuid", "website"]:
                    continue
                if key == "referer_type":
                    record["record"][key] = REFERRER_TYPES[
                        response.get(key, 1)
                    ]
                else:
                    record["record"][key] = str(response.get(key, 0))

            logs.log_json_obj(f"{record['stream']}.stdout", record)
            logs.stdout_json_obj(record)


def main() -> None:
    """Usual entry point."""

    # User interface
    def check_date(date: str) -> str:
        re_date = r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
        if not re.match(re_date, date):
            raise argparse.ArgumentTypeError(
                f"{date} does not have the correct format (yyyy-mm-dd)"
            )
        return date

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--end-date",
        type=check_date,
        required=True,
    )
    args = parser.parse_args()

    end_date = args.end_date

    for table, pattern, method in TABLE_LIST:
        # Write the schema for current table
        table["stream"] = pattern
        logs.log_json_obj(f"{table['stream']}.stdout", table)
        logs.stdout_json_obj(table)

        # Write records for current table
        write_records(copy.deepcopy(table), method, end_date)


if __name__ == "__main__":
    main()
