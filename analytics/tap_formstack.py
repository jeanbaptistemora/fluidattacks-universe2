"""
Singer tap for Formstack
"""

## pyhton3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import re
import json
import urllib.request

import logs
import api_formstack as API

# Long term goal:
#     singer tap to crawl the formstack forms
#         configurable
#         error resistant
#         historical and incremental
# Short term goal:
#     write the tap Output engine
#         write the RECORD Message
#             record. A JSON map containing a streamed data point
#             stream. The string name of the stream
#         write the SCHEMA Message
#         write the STATE  Message
# Medium term goal:
#     write support for the Config  input
#     write support for the State   input
#     write support for the Catalog input


def get_available_forms(user_token):
    """ retrieve a dictionary with all pairs {form_name: form_id} """
    params = {}
    params["page"] = "0"
    params["current_form"] = 0
    available_forms = {}

    while True:
        params["page"] = str(int(params["page"])+1)

        try:
            json_obj = API.get_all_forms(user_token, params)
        except urllib.error.HTTPError:
            break

        for form in json_obj["forms"]:
            params["current_form"] += 1
            form_name = form["name"].lower()
            form_name_std = ""
            for char in form_name:
                if char in "abcdefghijklmnopqrstuvwxyz ":
                    form_name_std += char
            available_forms[form_name_std] = form["id"]

    return available_forms


def write_queries(user_token, form_name, form_id):
    """ write queries needed for a given form so it can be fast accessed """
    params = {}
    params["page"] = "0"
    params["current_form"] = 0

    log_name = "tap_formstack." + form_name + ".json"
    log_name_pretty = "tap_formstack." + form_name + ".pretty.json"

    logs.initialize_log(log_name)
    logs.initialize_log(log_name_pretty)

    while True:
        params["page"] = str(int(params["page"])+1)

        try:
            json_obj = API.get_form_submissions(user_token, form_id, params)
        except urllib.error.HTTPError:
            break

        if params["current_form"] >= json_obj["total"]:
            break

        for submissions in json_obj["submissions"]:
            params["current_form"] += 1
            logs.log_json_obj(log_name, submissions, False)
            logs.log_json_obj(log_name_pretty, submissions, True)


def write_schema(form_name, stdout=True):
    """ write the SCHEMA message for a given form to stdout """

    stdout_json_obj = {}
    stdout_json_obj["type"] = "SCHEMA"
    stdout_json_obj["stream"] = form_name
    stdout_json_obj["key_properties"] = ["id"]
    stdout_json_obj["schema"] = {}
    stdout_json_obj["schema"]["properties"] = {}
    stdout_json_obj["schema"]["properties"]["id"] = {"type": "string"}

    log_name = "tap_formstack." + form_name + ".stdout.json"
    log_name_pretty = "tap_formstack." + form_name + ".pretty.stdout.json"

    file = open("./logs/tap_formstack." + form_name + ".json", "r")
    line = file.readline()
    while line:
        submission = json.loads(line)

        for key_d in submission["data"]:
            kind = submission["data"][key_d]["type"]
            name = submission["data"][key_d]["label"]
            value = submission["data"][key_d]["value"]

            if kind in ["text", "textarea", "name", "address", "email", "phone"]:
                stdout_json_obj["schema"]["properties"][name] = {"type": "string"}
            if kind in  ["select", "radio", "checkbox", "richtext", "embed"]:
                stdout_json_obj["schema"]["properties"][name] = {"type": "string"}
            if kind in ["number"]:
                stdout_json_obj["schema"]["properties"][name] = {"type": "number"}
            if kind in ["datetime"]:
                stdout_json_obj["schema"]["properties"][name] = {}
                stdout_json_obj["schema"]["properties"][name]["type"] = "string"
                stdout_json_obj["schema"]["properties"][name]["format"] = "date-time"
            if kind in ["file", "section", "product", "creditcard"]:
                pass
            if kind == "matrix":
                for inner_name in value:
                    padded_name = "[" + name + "][" + inner_name + "]"
                    stdout_json_obj["schema"]["properties"][padded_name] = {"type": "string"}

        line = file.readline()


    logs.log_json_obj(log_name, stdout_json_obj, False)
    logs.log_json_obj(log_name_pretty, stdout_json_obj, True)

    if stdout:
        stdout_json_str = json.dumps(stdout_json_obj)
        print(stdout_json_str)


def write_records(form_name, stdout=True):
    """ write all the RECORD messages for a given form to stdout """

    log_name = "tap_formstack." + form_name + ".stdout.json"
    log_name_pretty = "tap_formstack." + form_name + ".pretty.stdout.json"

    file = open("./logs/tap_formstack." + form_name + ".json", "r")
    line = file.readline()
    while line:
        submission = json.loads(line)

        stdout_json_obj = {}
        stdout_json_obj["type"] = "RECORD"
        stdout_json_obj["stream"] = form_name
        stdout_json_obj["record"] = {}
        stdout_json_obj["record"]["id"] = submission["id"]

        for key_d in submission["data"]:
            kind = submission["data"][key_d]["type"]
            name = submission["data"][key_d]["label"]
            value = submission["data"][key_d]["value"]

            if kind in ["text", "textarea", "name", "address", "email", "phone"]:
                stdout_json_obj["record"][name] = value
            if kind in  ["select", "radio", "checkbox", "richtext", "embed"]:
                stdout_json_obj["record"][name] = value
            if kind in ["number"]:
                try:
                    stdout_json_obj["record"][name] = std_number(value)
                except ExceptionIgnore:
                    pass
            if kind in ["datetime"]:
                try:
                    stdout_json_obj["record"][name] = std_date(value)
                except ExceptionIgnore:
                    pass
            if kind == "matrix" and isinstance(value, dict):
                for inner_name in value:
                    padded_name = "[" + name + "][" + inner_name + "]"
                    stdout_json_obj["record"][padded_name] = value[inner_name]
            if kind == "file":
                pass

        logs.log_json_obj(log_name, stdout_json_obj, False)
        logs.log_json_obj(log_name_pretty, stdout_json_obj, True)

        if stdout:
            stdout_json_str = json.dumps(stdout_json_obj)
            print(stdout_json_str)

        line = file.readline()


# this is not part of the tap but can be used to list all date-time formats in your formstack
# use this later to add transformation rules for date-time fields
def scan_dates(user_token, form_name, form_id):
    """ scan all the possible forms by date """

    params = {}
    params["page"] = "1"

    try:
        json_obj = API.get_form_submissions(user_token, form_id, params)
    except urllib.error.HTTPError:
        print("bad request")
        return

    for submissions in json_obj["submissions"]:
        stdout_json_obj = {}
        stdout_json_obj["form_name"] = form_name

        form_data = submissions["data"]
        for key_d in form_data:
            kind = form_data[key_d]["type"]
            name = form_data[key_d]["label"]
            value = form_data[key_d]["value"]

            if kind in ["datetime"]:
                stdout_json_obj[name] = {}
                stdout_json_obj[name]["raw"] = value
                stdout_json_obj[name]["mod"] = std_date(value)

        print(json.dumps(stdout_json_obj, indent=4))


def month_to_number(month):
    """ returns the month number for a given month name """
    correlation = {"jan": "01",
                   "feb": "02",
                   "mar": "03",
                   "apr": "04",
                   "may": "05",
                   "jun": "06",
                   "jul": "07",
                   "aug": "08",
                   "sep": "09",
                   "oct": "10",
                   "nov": "11",
                   "dec": "12"}
    for month_name, month_number in correlation.items():
        if month_name in month.lower():
            return month_number
    raise Exception("month not found in arguments (" + month + ")")


def std_date(date):
    """
    returns a json schema compliant date (RFC 3339)

    standard: https://tools.ietf.org/html/rfc3339#section-5.6
    """
    new_date = ""
    # Dec 31, 2018
    if re.match("([a-zA-Z]{3} [0-9]{2}, [0-9]{4})", date):
        new_date = date[8:12] + "-"
        new_date += month_to_number(date[0:3]) + "-"
        new_date += date[4:6] + "T00:00:00Z"
    # 2018 12 31 or 2018/12/31 or 2018-12-31
    elif re.match("([0-9]{4}( |/|-)[0-9]{2}( |/|-)[0-9]{2})", date):
        new_date = date[0:10] + "T00:00:00Z"
    # 12 31 2018 or 12/31/2018 or 12-31-2018
    elif re.match("([0-9]{2}( |/|-)[0-9]{2}( |/|-)[0-9]{4})", date):
        new_date = date[6:10] + "-" + date[3:5] + "-" + date[0:2] + "T00:00:00Z"
    # Nov 2024
    elif re.match("([a-zA-Z]{3} [0-9]{4})", date):
        new_date = date[-4:] + "-"
        new_date += month_to_number(date[0:3]) + "-"
        new_date += "01T00:00:00Z"
    # 19:27
    elif re.match("([0-9]{2}:[0-9]{2})", date):
        new_date = "1900-01-01T" + date + ":00Z"
    # User didn't fill the field
    elif date == "":
        new_date = "1900-01-01T00:00:00Z"
    # Not found
    else:
        raise Exception("Unrecognized Date Format (" + date + ")")
    return new_date


def std_number(number):
    """ returns a json schema compliant number """
    # discovered data quality problems
    number = number.replace(",", ".")

    new_number = ""
    for char in number:
        if char in "01234567890.":
            new_number += char
    number = new_number

    if not number:
        return 0.0

    try:
        number = float(number)
    except:
        raise ExceptionIgnore

    return number

class ExceptionIgnore(Exception):
    """ Raised when tap should ignore the input """
