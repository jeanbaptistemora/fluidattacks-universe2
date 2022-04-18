"""Singer tap for the Timedoctor API."""

import argparse
import datetime
import json
import re
import sys
from tap_timedoctor import (
    logs,
)
from tap_timedoctor.api import (
    Options,
    Worker,
)
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    Tuple,
)
import unicodedata

# Type aliases that improve clarity
JSON = Any

_TYPE_STRING: JSON = {"type": "string"}
_TYPE_NUMBER: JSON = {"type": "number"}
_TYPE_DATE: JSON = {"type": "string", "format": "date-time"}


def standard_name(name: str) -> str:
    """Remove heading and trailing whitespaces.

    Puts exactly one space between words and get rid of ñ and accent marks.
    """
    unic = unicodedata.normalize
    std = " ".join(name.split())
    std = (unic("NFKD", std).encode("ASCII", "ignore")).lower().decode("utf-8")
    return std


def ensure_200(status_code: Optional[int]) -> None:
    """Ensure status_code 200 or exit."""
    if not status_code == 200:
        print(f"INFO: Timedoctor API, ERROR {status_code}")
        print("          The service is probably down.")
        print("         You should run this script again later.")
        sys.exit(1)


def translate_date(date_obj: Any) -> str:
    """Translate a date-time value to RFC3339 format."""
    date_obj = str(date_obj)
    if re.match(r"\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}\.\d+", date_obj):
        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S.%f")
    elif re.match(r"\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}", date_obj):
        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S")
    elif isinstance(date_obj, (int, float)):
        date_obj = datetime.datetime.utcfromtimestamp(date_obj)
    else:
        try:
            date_obj = datetime.datetime.utcfromtimestamp(int(date_obj))
        except ValueError:
            date_obj = datetime.datetime(1900, 1, 1, 0, 0, 0)

    return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")


def sync_worklogs(
    api_worker: Worker,
    company_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> None:
    """API version 1.1.

    https://webapi.timedoctor.com/doc#worklogs
    """

    def write_schema() -> None:
        """Write the schema for this table."""
        schema: JSON = {
            "type": "SCHEMA",
            "stream": "worklogs",
            "key_properties": ["worklog_id"],
            "schema": {
                "properties": {
                    "worklog_id": _TYPE_STRING,
                    "length": _TYPE_NUMBER,
                    "user_id": _TYPE_STRING,
                    "user_name": _TYPE_STRING,
                    "task_id": _TYPE_STRING,
                    "task_name": _TYPE_STRING,
                    "project_id": _TYPE_STRING,
                    "project_name": _TYPE_STRING,
                    "start_time": _TYPE_DATE,
                    "end_time": _TYPE_DATE,
                    "edited": _TYPE_STRING,
                    "work_mode": _TYPE_STRING,
                }
            },
        }
        logs.log_json_obj("worklogs.stdout", schema)
        logs.stdout_json_obj(schema)

    def write_records() -> None:
        """Write the records for this table."""

        def translate_work_mode(work_mode: str) -> str:
            work_mode_map: JSON = {
                "0": "online",
                "1": "on chat",
                "2": "on chat",
                "3": "offline or afk",
                "4": "on break",
                "5": "on break",
                "6": "manually added",
                "7": "mobile app",
            }
            work_mode_str: str = work_mode_map.get(work_mode, "other")
            return work_mode_str

        limit: int = 500
        offset: int = 0

        # the API doesn't provide a way to deterministically stop
        #   iterate until an empty list is found
        while 1:
            status_code, response = api_worker.get_worklogs(
                company_id, offset, Options(limit, start_date, end_date)
            )
            ensure_200(status_code)
            worklogs: JSON = json.loads(response)["worklogs"]

            logs.log_json_obj("worklogs", worklogs)

            if not worklogs["items"]:
                break

            for worklog in worklogs["items"]:
                record: JSON = {
                    "type": "RECORD",
                    "stream": "worklogs",
                    "record": {
                        "worklog_id": worklog.get("id", ""),
                        "length": float(worklog.get("length", "0.0")),
                        "user_id": worklog.get("user_id", ""),
                        "user_name": standard_name(
                            worklog.get("user_name", "")
                        ),
                        "task_id": worklog.get("task_id", ""),
                        "task_name": worklog.get("task_name", ""),
                        "project_id": worklog.get("project_id", ""),
                        "project_name": worklog.get("project_name", ""),
                        "start_time": translate_date(
                            worklog.get("start_time", "")
                        ),
                        "end_time": translate_date(
                            worklog.get("end_time", "")
                        ),
                        "edited": worklog.get("edited", ""),
                        "work_mode": translate_work_mode(
                            worklog.get("work_mode", "")
                        ),
                    },
                }

                logs.log_json_obj("worklogs.stdout", record)
                logs.stdout_json_obj(record)

            offset += limit

    write_schema()
    write_records()


def sync_computer_activity(
    api_worker: Worker,
    company_id: str,
    users_list: Iterator[Tuple[str, str]],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> None:
    """Sync computer activity using API version 1.1.

    https://webapi.timedoctor.com/doc#screenshots
    """

    def write_schema() -> None:
        """Write the schema for this table."""
        schema: JSON = {
            "type": "SCHEMA",
            "stream": "computer_activity",
            "key_properties": ["uuid"],
            "schema": {
                "properties": {
                    "uuid": _TYPE_STRING,
                    "date": _TYPE_DATE,
                    "user_id": _TYPE_STRING,
                    "user_name": _TYPE_STRING,
                    "task_id": _TYPE_STRING,
                    "project_id": _TYPE_STRING,
                    "process": _TYPE_STRING,
                    "window": _TYPE_STRING,
                    "keystrokes": _TYPE_NUMBER,
                    "mousemovements": _TYPE_NUMBER,
                    "deleted_by": _TYPE_STRING,
                    "deletedSeconds": _TYPE_NUMBER,
                }
            },
        }
        logs.log_json_obj("computer_activity.stdout", schema)
        logs.stdout_json_obj(schema)

    def write_records(user_id: str, user_name: str) -> None:
        """Write the records for this table."""

        def sass(obj: JSON, keys: List[str], default: Any) -> Any:
            """Safely get the nested value after accessing a dict."""
            for key in keys:
                obj = obj.get(key, None) if isinstance(obj, dict) else obj
            return default if obj is None else obj

        (status_code, response) = api_worker.get_computer_activity(
            company_id, user_id, Options(20000, start_date, end_date)
        )
        ensure_200(status_code)

        response_obj: JSON = json.loads(response)

        logs.log_json_obj("computer_activity", response_obj)

        # There is only one item in response
        computer_activity = response_obj[0].get("screenshots", [])
        if computer_activity:
            computer_activity = computer_activity.get("screenshots", [])

        for record in computer_activity:
            stdout_json_obj: JSON = {
                "type": "RECORD",
                "stream": "computer_activity",
                "record": {
                    "uuid": record["uuid"],
                    "date": translate_date(record["date"]),
                    "task_id": str(record["task_id"]),
                    "project_id": record["project_name"],
                    "user_id": user_id,
                    "user_name": user_name,
                    "keystrokes": record["keystrokes"],
                    "mousemovements": record["mousemovements"],
                },
            }

            stdout_json_obj["record"]["process"] = sass(
                record, ["appInfo", "process"], ""
            )
            stdout_json_obj["record"]["window"] = sass(
                record, ["appInfo", "window"], ""
            )
            stdout_json_obj["record"]["deleted_by"] = sass(
                record, ["deleted_by"], ""
            )
            stdout_json_obj["record"]["deletedSeconds"] = sass(
                record, ["deletedSeconds"], 0.0
            )

            logs.log_json_obj("computer_activity.stdout", stdout_json_obj)
            logs.stdout_json_obj(stdout_json_obj)

    write_schema()
    for user_id, user_name in users_list:
        write_records(user_id, user_name)


def main() -> None:
    """Usual entry point."""

    # user interface
    def check_date(date: str) -> str:
        re_date = r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
        if not re.match(re_date, date):
            raise argparse.ArgumentTypeError(
                f"{date} does not have the correct format (yyyy-mm-dd)"
            )
        return date

    # by default all the data from a year ago is extracted
    today = datetime.date.today()
    start_date = today.replace(today.year - 1).isoformat()
    end_date = today.isoformat()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--auth",
        required=True,
        help="JSON authentication file",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-s",
        "--start-date",
        type=check_date,
        required=False,
        default=start_date,
    )
    parser.add_argument(
        "-e", "--end-date", type=check_date, required=False, default=end_date
    )
    parser.add_argument("--work-logs", "-w", action="store_true")
    parser.add_argument("--computer-activity", "-ca", action="store_true")
    args = parser.parse_args()

    start_date = args.start_date or start_date
    end_date = args.end_date or end_date

    access_token: str = json.load(args.auth)["access_token"]
    api_worker = Worker(access_token)

    # get some account info by inspecting the admin account (the token owner)
    (status_code, response) = api_worker.get_companies()
    ensure_200(status_code)
    account_info: dict = json.loads(response)["user"]
    company_id = str(account_info["company_id"])

    # get the id of all users in the company
    (status_code, response) = api_worker.get_users(company_id)
    ensure_200(status_code)

    # sync
    if args.work_logs:
        sync_worklogs(api_worker, company_id, start_date, end_date)
    if args.computer_activity:
        users: Iterator[Tuple[str, str]] = map(
            lambda x: (str(x["user_id"]), x["full_name"]),
            json.loads(response)["users"],
        )
        sync_computer_activity(
            api_worker,
            company_id,
            users,
            start_date=start_date,
            end_date=end_date,
        )


if __name__ == "__main__":
    main()
