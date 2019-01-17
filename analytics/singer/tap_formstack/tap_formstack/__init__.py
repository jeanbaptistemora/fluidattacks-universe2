"""
Singer tap for Formstack
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import re
import sys
import json
import argparse
import urllib.request

from . import logs
from . import api_formstack as API

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

_TYPE_STRING = {"type": "string"}
_TYPE_NUMBER = {"type": "number"}
_TYPE_DATE = {"type": "string", "format": "date-time"}

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
            form_name_std = std_text(form["name"])
            available_forms[form_name_std] = form["id"]

    return available_forms

def write_queries(user_token, form_name, form_id):
    """ write queries needed for a given form so it can be fast accessed """
    params = {}
    params["page"] = "0"
    params["current_form"] = 0

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
            logs.log_json_obj(form_name, submissions)

def write_schema(form_name, stdout=True):
    """ write the SCHEMA message for a given form to stdout """

    def assign_to_checkbox(json_obj, data):
        """ handles the assignment of data to the json_obj """
        name = data["label"]
        value = data["value"]
        if isinstance(value, str):
            padded_name = "checkbox[" + name + "][" + value + "]"
            stdout_json_obj["schema"]["properties"][padded_name] = _TYPE_STRING
        else:
            for inner_name in value:
                padded_name = "checkbox[" + name + "][" + inner_name + "]"
                stdout_json_obj["schema"]["properties"][padded_name] = _TYPE_STRING
        return json_obj

    def assign_to_matrix(json_obj, data):
        """ handles the assignment of data to the json_obj """
        name = data["label"]
        value = data["value"]
        if isinstance(value, str):
            padded_name = "matrix[" + name + "][" + value + "]"
            stdout_json_obj["schema"]["properties"][padded_name] = _TYPE_STRING
        else:
            for inner_name in value:
                padded_name = "matrix[" + name + "][" + inner_name + "]"
                stdout_json_obj["schema"]["properties"][padded_name] = _TYPE_STRING
        return json_obj

    stdout_json_obj = {
        "type": "SCHEMA",
        "stream": form_name,
        "key_properties": ["_form_unique_id"],
        "schema": {
            "properties": {
                "_form_unique_id": _TYPE_STRING,
                "_read": _TYPE_NUMBER,
                "_timestamp": _TYPE_DATE,
                "_latitude": _TYPE_NUMBER,
                "_longitude": _TYPE_NUMBER,
                "_user_agent": _TYPE_STRING,
                "_remote_addr": _TYPE_STRING
            }
        }
    }

    file = open(logs.DOMAIN + form_name + ".json", "r")
    line = file.readline()
    while line:
        submission = json.loads(line)

        for key_d in submission["data"]:
            kind = submission["data"][key_d]["type"]
            name = submission["data"][key_d]["label"]

            if not name in stdout_json_obj["schema"]["properties"]:
                if kind in ["text", "textarea", "name", "address", "email", "phone"]:
                    stdout_json_obj["schema"]["properties"][name] = _TYPE_STRING
                elif kind in ["select", "radio", "richtext", "embed", "creditcard"]:
                    stdout_json_obj["schema"]["properties"][name] = _TYPE_STRING
                elif kind in ["file", "image"]:
                    stdout_json_obj["schema"]["properties"][name] = _TYPE_STRING
                elif kind in ["number"]:
                    stdout_json_obj["schema"]["properties"][name] = _TYPE_NUMBER
                elif kind in ["datetime"]:
                    stdout_json_obj["schema"]["properties"][name] = _TYPE_DATE

            if kind in ["matrix"]:
                stdout_json_obj = assign_to_matrix(stdout_json_obj, submission["data"][key_d])
            elif kind in ["checkbox"]:
                stdout_json_obj = assign_to_checkbox(stdout_json_obj, submission["data"][key_d])

        line = file.readline()

    logs.log_json_obj(form_name + ".stdout", stdout_json_obj)

    if stdout:
        print(json.dumps(stdout_json_obj))

    return stdout_json_obj["schema"]["properties"]

def write_records(form_name, schema_properties, stdout=True):
    """ write all the RECORD messages for a given form to stdout """

    def assign_to_checkbox(json_obj, data):
        """ handles the assignment of data to the json_obj """
        name = data["label"]
        value = data["value"]
        if isinstance(value, str):
            padded_name = "checkbox[" + name + "][" + value + "]"
            json_obj["record"][padded_name] = "selected"
        elif isinstance(value, list):
            for inner_name in value:
                padded_name = "checkbox[" + name + "][" + inner_name + "]"
                json_obj["record"][padded_name] = "selected"

        return json_obj

    def assign_to_matrix(json_obj, data):
        """ handles the assignment of data to the json_obj """
        name = data["label"]
        value = data["value"]
        if isinstance(value, str):
            padded_name = "matrix[" + name + "][" + value + "]"
            json_obj["record"][padded_name] = value
        elif isinstance(value, dict):
            for inner_name in value:
                padded_name = "matrix[" + name + "][" + inner_name + "]"
                json_obj["record"][padded_name] = value[inner_name]

        return json_obj

    file = open(logs.DOMAIN + form_name + ".json", "r")
    line = file.readline()

    while line:
        submission = json.loads(line)

        stdout_json_obj = {
            "type": "RECORD",
            "stream": form_name,
            "record": {
                "_form_unique_id": submission.get("id", ""),
                "_read": std_number(submission.get("read"), default=0.0),
                "_latitude": std_number(submission.get("latitude"), default=0.0),
                "_longitude": std_number(submission.get("longitude"), default=0.0),
                "_timestamp": std_date(submission.get("timestamp"), default="1900-01-01T00:00:00Z"),
                "_user_agent": submission.get("user_agent", ""),
                "_remote_addr": submission.get("remote_addr", "")
            }
        }

        for key_d in submission["data"]:
            record_kind = submission["data"][key_d]["type"]

            if record_kind in ["matrix"]:
                stdout_json_obj = assign_to_matrix(stdout_json_obj, submission["data"][key_d])
            elif record_kind in ["checkbox"]:
                stdout_json_obj = assign_to_checkbox(stdout_json_obj, submission["data"][key_d])
            else:
                try:
                    name = submission["data"][key_d]["label"]
                    value = submission["data"][key_d]["value"]
                    flat_value = submission["data"][key_d]["flat_value"]

                    if schema_properties[name] == _TYPE_STRING:
                        stdout_json_obj["record"][name] = flat_value
                    elif schema_properties[name] == _TYPE_NUMBER:
                        stdout_json_obj["record"][name] = std_number(value)
                    elif schema_properties[name] == _TYPE_DATE:
                        stdout_json_obj["record"][name] = std_date(value)
                except UnrecognizedNumber:
                    logs.log_error("number: [" + value + "]")
                except UnrecognizedDate:
                    logs.log_error("date:   [" + value + "]")

        logs.log_json_obj(form_name + ".stdout", stdout_json_obj)

        if stdout:
            print(json.dumps(stdout_json_obj))

        line = file.readline()

def std_text(text):
    """ returns a CDN compliant text """

    # log it
    logs.log_conversions("text [" + text + "]")

    # always lowercase
    text = text.lower()

    # no accent marks
    to_replace = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u"
    }

    for old_char, new_char in to_replace.items():
        text = text.replace(old_char, new_char)

    # just letters and spaces
    new_text = ""
    for char in text:
        if char in "abcdefghijklmnopqrstuvwxyz ":
            new_text += char

    # log it
    logs.log_conversions("     [" + new_text + "]")

    return new_text

def std_date(date, default=None):
    """
    returns a json schema compliant date (RFC 3339)

    standard: https://tools.ietf.org/html/rfc3339#section-5.6
    """

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
        return "err"

    # log it
    logs.log_conversions("date [" + date + "]")

    new_date = ""
    # Dec 31, 2018
    if re.match("([a-zA-Z]{3} [0-9]{2}, [0-9]{4})", date):
        new_date = date[8:12] + "-"
        new_date += month_to_number(date[0:3]) + "-"
        new_date += date[4:6] + "T00:00:00Z"
    # 2018 12 31 or 2018/12/31 or 2018-12-31
    elif re.match("([0-9]{4}( |/|-)(01|02|03|04|05|06|07|08|09|10|11|12)( |/|-)[0-9]{2})", date):
        new_date = date[0:10] + "T00:00:00Z"
    # 12 31 2018 or 12/31/2018 or 12-31-2018
    elif re.match("((01|02|03|04|05|06|07|08|09|10|11|12)( |/|-)[0-9]{2}( |/|-)[0-9]{4})", date):
        new_date = date[6:10] + "-" + date[0:2] + "-" + date[3:5] + "T00:00:00Z"
    # Nov 2024
    elif re.match("([a-zA-Z]{3} [0-9]{4})", date):
        new_date = date[4:8] + "-"
        new_date += month_to_number(date[0:3]) + "-"
        new_date += "01T00:00:00Z"
    # 19:27 represents an hour
    elif re.match("([0-9]{2}:[0-9]{2})", date):
        new_date = "1900-01-01T" + date[0:5] + ":00Z"
    # User didn't fill the field
    elif not date:
        new_date = "1900-01-01T00:00:00Z"
    # User supplied default value
    elif default is not None:
        new_date = default
    # Not possible to match, hit the panic button
    else:
        raise UnrecognizedDate

    # log it
    logs.log_conversions("     [" + new_date + "]")

    return new_date

def std_number(number, default=None):
    """ returns a json schema compliant number """
    # log it
    logs.log_conversions("number [" + str(number) + "]")

    # type null instead of str
    if not isinstance(number, str):
        return 0.0

    # point is the decimal separator
    number = number.replace(",", ".")

    # clean typos
    new_number = ""
    for char in number:
        if char in "+-01234567890.":
            new_number += char
    number = new_number

    # seems ok, lets try
    try:
        number = float(number)
    except ValueError:
        if default is None:
            raise UnrecognizedNumber
        else:
            number = default

    # log it
    logs.log_conversions("       [" + str(number) + "]")

    return number

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

class UnrecognizedString(Exception):
    """ Raised when tap didn't find a conversion """

class UnrecognizedNumber(Exception):
    """ Raised when tap didn't find a conversion """

class UnrecognizedDate(Exception):
    """ Raised when tap didn't find a conversion """

def arguments_error(parser):
    """ Print help and exit """
    parser.print_help()
    exit(1)

def main():
    """ usual entry point """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--auth',
        help='JSON authentication file',
        type=argparse.FileType('r'))
    parser.add_argument(
        '-c', '--conf',
        help='JSON configuration file',
        type=argparse.FileType('r'))
    args = parser.parse_args()

    if not args.auth:
        arguments_error(parser)

    formstack_token = json.load(args.auth).get("token")

    if not formstack_token:
        arguments_error(parser)

    tap_conf = {}
    if args.conf:
        tap_conf = json.load(args.conf)

    # ==== Formstack  ==========================================================
    # get the available forms in the account
    available_forms = get_available_forms(formstack_token)

    # forms after merge
    real_forms = set()

    for form_name, form_id in available_forms.items():
        # first download, it won't download encrypted/archived forms
        if form_name in tap_conf.get("alias", []):
            alias = tap_conf["alias"].get(form_name)
            write_queries(formstack_token, alias, form_id)
            real_forms.add(alias)
        else:
            write_queries(formstack_token, form_name, form_id)
            real_forms.add(form_name)

    for form_name in real_forms:
        try:
            form_schema = write_schema(form_name)
            write_records(form_name, form_schema)
        # Given an encrypted form is not downloaded
        # Then the file doesn't exist
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    main()
