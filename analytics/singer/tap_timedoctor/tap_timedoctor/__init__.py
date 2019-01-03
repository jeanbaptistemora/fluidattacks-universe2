"""
Singer tap for the Timedoctor's API
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import re
import json
import argparse
import datetime
import urllib.request

from . import logs
from . import api_timedoctor

_TYPE_STRING = {"type": "string"}
_TYPE_NUMBER = {"type": "number"}
_TYPE_DATE = {"type": "string", "format": "date-time"}

def get_users_list(timedoctor_users_str):
    """ parses the users response into a list of users """
    def parse(user):
        """
        parses the user information from the raw response
            FA Fluid Activo (incluidos insourcing, opción por defecto, por ende dejar vacio)
            FR Fluid Retirado
            AR Autonomic Activo
            AR Autonomic Retirado
            IA Inmersión Activo
            IR Inmersión Retirado (no contratado, si contratado pasa a FA o FR)
        """

        user_full_name = user["full_name"]
        user_id = str(user["user_id"])
        user_email = user["email"]

        user_tokens = user_full_name.split()
        user_status = user_tokens[-1].upper()

        if user_status in ["FR", "AA", "AR", "IA", "IR"]:
            user_name = " ".join(user_tokens[0:-1])
        else:
            user_name = " ".join(user_tokens)
            user_status = "FA"
        return (user_id, user_email, user_name, user_status)

    users = json.loads(timedoctor_users_str)["users"]
    users_list = list(map(parse, users))
    users_map = {i: {"email": e, "name": n, "status": s} for i, e, n, s in users_list}
    return users_list, users_map

def ensure_200(status_code):
    """ Timedoctor's API have a lot of downtimes throughout the day, ensure 200 or exit """
    if not status_code == 200:
        print("INFO: Timedoctor API, ERROR " + str(status_code))
        print("          the service is probably down, you should run this script again later")
        exit(1)

def translate_date(date_str):
    """ translates a date-time value from the timedoctor format to RFC3339 format """
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        date_str = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        date_str = "1900-01-01T00:00:00Z"
    return date_str

def sync_worklogs(api_worker, company_id, users_map):
    """ API version 1.1
            https://webapi.timedoctor.com/doc#worklogs """

    def write_schema():
        """ write the schema for this table """

        stdout_json_obj = {
            "type": "SCHEMA",
            "stream": "worklogs",
            "key_properties": ["worklog_id"],
            "schema": {
                "properties": {
                    "worklog_id": _TYPE_STRING,
                    "length": _TYPE_NUMBER,
                    "user_id": _TYPE_STRING,
                    "user_name": _TYPE_STRING,
                    "user_email": _TYPE_STRING,
                    "user_status": _TYPE_STRING,
                    "task_id": _TYPE_STRING,
                    "task_name": _TYPE_STRING,
                    "project_id": _TYPE_STRING,
                    "project_name": _TYPE_STRING,
                    "start_time": _TYPE_DATE,
                    "end_time": _TYPE_DATE,
                    "edited": _TYPE_STRING,
                    "work_mode": _TYPE_STRING,
                }
            }
        }
        logs.log_json_obj("worklogs.stdout", stdout_json_obj)
        print(json.dumps(stdout_json_obj))
    def write_records():
        """ write the records for this table """
        def translate_work_mode(work_mode):
            work_mode_map = {
                "0": "online",
                "1": "on chat", # legacy
                "2": "on chat", # legacy
                "3": "offline or afk",
                "4": "on break",
                "5": "on break",
                "6": "manually added",
                "7": "mobile app"
            }
            work_mode_str = work_mode_map.get(work_mode, "other")
            return work_mode_str

        limit = 500
        offset = 0

        # the API doesn't provide a way to deterministically stop
        #   iterate until an empty list is found
        while 1:
            (status_code, response) = api_worker.get_worklogs(company_id, limit, offset)
            ensure_200(status_code)
            worklogs = json.loads(response)["worklogs"]

            logs.log_json_obj("worklogs", worklogs)

            if not worklogs["items"]:
                break

            for worklog in worklogs["items"]:
                user_id = worklog.get("user_id", "")
                user_name = worklog.get("user_name", "")
                user_email = ""
                user_status = ""
                if user_id in users_map:
                    user_info = users_map[user_id]
                    user_name = user_info.get("name", "")
                    user_email = user_info.get("email", "")
                    user_status = user_info.get("status", "")

                stdout_json_obj = {
                    "type": "RECORD",
                    "stream": "worklogs",
                    "record": {
                        "worklog_id": worklog.get("id", ""),
                        "length": float(worklog.get("length", "0.0")),
                        "user_id": user_id,
                        "user_name": user_name,
                        "user_email": user_email,
                        "user_status": user_status,
                        "task_id": worklog.get("task_id", ""),
                        "task_name": worklog.get("task_name", ""),
                        "project_id": worklog.get("project_id", ""),
                        "project_name": worklog.get("project_name", ""),
                        "start_time": translate_date(worklog.get("start_time", "")),
                        "end_time": translate_date(worklog.get("end_time", "")),
                        "edited": worklog.get("edited", ""),
                        "work_mode": translate_work_mode(worklog.get("work_mode", "")),
                    }
                }

                logs.log_json_obj("worklogs.stdout", stdout_json_obj)
                print(json.dumps(stdout_json_obj))

            offset += limit

    write_schema()
    write_records()

def sync_computer_activity(api_worker, company_id, users_list):
    """ API version 1.1
            https://webapi.timedoctor.com/doc#screenshots """

    def write_schema():
        """ write the schema for this table """

        stdout_json_obj = {
            "type": "SCHEMA",
            "stream": "computer_activity",
            "key_properties": ["uuid"],
            "schema": {
                "properties": {
                    "uuid": _TYPE_STRING,
                    "date": _TYPE_DATE,

                    "user_id": _TYPE_STRING,
                    "user_email": _TYPE_STRING,
                    "user_name": _TYPE_STRING,
                    "user_status": _TYPE_STRING,

                    "task_id": _TYPE_STRING,
                    "project_id": _TYPE_STRING,

                    "process": _TYPE_STRING,
                    "window": _TYPE_STRING,


                    "keystrokes": _TYPE_NUMBER,
                    "mousemovements": _TYPE_NUMBER,

                    "deleted_by": _TYPE_STRING,
                    "deletedSeconds": _TYPE_NUMBER,
                }
            }
        }
        logs.log_json_obj("computer_activity.stdout", stdout_json_obj)
        print(json.dumps(stdout_json_obj))
    def write_records(user_id, user_email, user_name, user_status):
        """ write the records for this table """
        def sass(obj, keys, default):
            """ safely get the nested value after accessing a dict sucessively """
            for key in keys:
                if isinstance(obj, dict):
                    obj = obj.get(key, None)
            return default if obj is None else obj

        (status_code, response) = api_worker.get_computer_activity(company_id, user_id)
        ensure_200(status_code)
        response_obj = json.loads(response)

        logs.log_json_obj("computer_activity", response_obj)

        computer_activity = response_obj[0]["screenshots"]

        for record in computer_activity:
            stdout_json_obj = {
                "type": "RECORD",
                "stream": "computer_activity",
                "record": {
                    "uuid": record["id"]["uuid"],
                    "date": translate_date(record["date"]["date"]),

                    "task_id": str(record["task_id"]),
                    "project_id": record["project_id"],

                    "keystrokes": record["keystrokes"],
                    "mousemovements": record["mousemovements"],
                }
            }

            stdout_json_obj["record"]["user_id"] = user_id
            stdout_json_obj["record"]["user_email"] = user_email
            stdout_json_obj["record"]["user_name"] = user_name
            stdout_json_obj["record"]["user_status"] = user_status

            stdout_json_obj["record"]["process"] = sass(record, ["appInfo", "process"], "")
            stdout_json_obj["record"]["window"] = sass(record, ["appInfo", "window"], "")
            stdout_json_obj["record"]["deleted_by"] = sass(record, ["deleted_by"], "")
            stdout_json_obj["record"]["deletedSeconds"] = sass(record, ["deletedSeconds"], 0.0)

            logs.log_json_obj("computer_activity.stdout", stdout_json_obj)
            print(json.dumps(stdout_json_obj))

    write_schema()
    for user in users_list:
        user_id, user_email, user_name, user_status = user
        write_records(user_id, user_email, user_name, user_status)

def arguments_error(parser):
    """ Print help and exit """
    parser.print_help()
    exit(1)

def main():
    """ usual entry point """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-auth',
        help='JSON authentication file',
        type=argparse.FileType('r'))
    args = parser.parse_args()

    if not args.auth:
        arguments_error(parser)

    access_token = json.load(args.auth).get("access_token")

    if not access_token:
        arguments_error(parser)

    # ==== Time Doctor ========================================================
    api_worker = api_timedoctor.Worker(access_token)

    # get some account info by inspecting the admin account (the token owner)
    (status_code, response) = api_worker.get_companies()
    ensure_200(status_code)
    account_info = json.loads(response)["user"]
    company_id = str(account_info["company_id"])

    # get the id of all users in the company
    (status_code, response) = api_worker.get_users(company_id)
    ensure_200(status_code)
    users_list, users_map = get_users_list(response)

    # sync
    sync_worklogs(api_worker, company_id, users_map)
    sync_computer_activity(api_worker, company_id, users_list)

if __name__ == "__main__":
    main()
