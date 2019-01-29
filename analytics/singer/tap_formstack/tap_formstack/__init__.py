"""Singer tap for the Formstack API.
"""

import re
import json
import argparse
import datetime
import urllib.error
import urllib.request

from typing import Callable, Iterable, Dict, Tuple, Any

from . import logs

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

# Type aliases that improve clarity
JSON = Any


API_URL = f"https://www.formstack.com/api/v2"

_TYPE_STRING = {"type": "string"}
_TYPE_NUMBER = {"type": "number"}
_TYPE_DATE = {"type": "string", "format": "date-time"}


class UnrecognizedString(Exception):
    """Raised when tap didn't find a conversion.
    """


class UnrecognizedNumber(Exception):
    """Raised when tap didn't find a conversion.
    """


class UnrecognizedDate(Exception):
    """Raised when tap didn't find a conversion.
    """


def iter_lines(file_name: str, function: Callable) -> Iterable[Any]:
    """Yields function(line) on every line of a file.

    Args:
        file_name: The name of the file whose lines we are to iterate.
        function: A function to apply to each line.

    Yields:
        function(line) on every line of the file with file_name.
    """

    with open(file_name, "r") as file:
        for line in file:
            yield function(line)


def get_request_response(user_token: str, resource: str) -> JSON:
    """Makes a request for a resource.

    Returns:
        A json object with the response.
    """

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token}"
    }
    request = urllib.request.Request(resource, headers=headers)
    response = urllib.request.urlopen(request).read().decode('utf-8')
    json_obj = json.loads(response)
    return json_obj


def get_page_of_forms(user_token: str, **kwargs: Any) -> JSON:
    """Get a page of forms in the account.
    """

    page = kwargs["page"]
    resource = f"{API_URL}/form.json?page={page}&per_page=100"
    return get_request_response(user_token, resource)


def get_form_submissions(user_token: str, form_id: str, **kwargs: Any) -> JSON:
    """ get all submissions made for the specified form_id """

    page = kwargs["page"]
    resource = f"{API_URL}/form/{form_id}/submission.json?page={page}"
    resource += "&min_time=0000-01-01&max_time=2100-12-31"
    resource += "&expand_data=0"
    resource += "&per_page=100"
    resource += "&sort=DESC"
    resource += "&data=0"
    json_obj = get_request_response(user_token, resource)
    return json_obj


def get_available_forms(user_token: str) -> Dict[str, str]:
    """Retrieves a dictionary with all pairs {form_name: form_id}.
    """

    page: int = 0
    available_forms: Dict[str, str] = {}

    while 1:
        page += 1

        try:
            json_obj = get_page_of_forms(user_token, page=page)
        except urllib.error.HTTPError:
            break

        for form in json_obj["forms"]:
            form_name_std = std_text(form["name"])
            available_forms[form_name_std] = form["id"]

    return available_forms


def write_queries(user_token: str, form_name: str, form_id: str) -> None:
    """Write queries needed for a given form so it can be fast accessed.
    """

    page: int = 0
    current_form: int = 0

    while 1:
        page += 1

        try:
            json_obj = get_form_submissions(user_token, form_id, page=page)
        except urllib.error.HTTPError:
            break

        if current_form >= json_obj["total"]:
            break

        for submissions in json_obj["submissions"]:
            current_form += 1
            logs.log_json_obj(form_name, submissions)


def write_schema(form_name: str) -> JSON:
    """Write the SCHEMA message for a given form to stdout.
    """

    schema: JSON = {
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

    fields_type: JSON = {
        "string": [
            "text", "textarea", "name", "address", "email", "phone", "select",
            "radio", "richtext", "embed", "creditcard", "file", "image"
        ],
        "number": [
            "number"
        ],
        "date": [
            "datetime"
        ],
        "nested": [
            "matrix", "checkbox"
        ]
    }

    file_name = f"{logs.DOMAIN}{form_name}.jsonstream"
    for submission in iter_lines(file_name, json.loads):
        for key_d in submission["data"]:
            field_type: str = submission["data"][key_d]["type"]
            field_name: str = submission["data"][key_d]["label"]

            if field_name not in schema["schema"]["properties"]:
                if field_type in fields_type["string"]:
                    schema["schema"]["properties"][field_name] = _TYPE_STRING
                elif field_type in fields_type["number"]:
                    schema["schema"]["properties"][field_name] = _TYPE_NUMBER
                elif field_type in fields_type["date"]:
                    schema["schema"]["properties"][field_name] = _TYPE_DATE

            # mutable object on function call == pass by reference
            if field_type in fields_type["nested"]:
                write_schema__denest(
                    schema, submission["data"][key_d], field_type)

    logs.log_json_obj(f"{form_name}.stdout", schema)
    logs.stdout_json_obj(schema)

    return schema["schema"]["properties"]


def write_schema__denest(schema: JSON, data: JSON, nesting_type: str) -> None:
    """Handles the assignment of a nested field to the schema.

    Good examples of nested fields are matrix and checkbox.
    """

    name = data["label"]
    value = data["value"]
    if isinstance(value, str):
        padded_name = f"{nesting_type}[{name}][{value}]"
        schema["schema"]["properties"][padded_name] = _TYPE_STRING
    else:
        for inner_name in value:
            padded_name = f"{nesting_type}[{name}][{inner_name}]"
            schema["schema"]["properties"][padded_name] = _TYPE_STRING


def write_records(form_name: str, schema_properties: JSON) -> None:
    """Write all records for a given form to stdout.
    """

    file_name: str = f"{logs.DOMAIN}{form_name}.jsonstream"
    for submission in iter_lines(file_name, json.loads):
        record: JSON = write_records__assign_data(
            form_name,
            schema_properties,
            submission)
        logs.log_json_obj(f"{form_name}.stdout", record)
        logs.stdout_json_obj(record)


def write_records__assign_data(
        form_name: str,
        schema_properties: JSON,
        submission: JSON) -> JSON:
    """Handles the assignment of form data to a record.
    """

    record: JSON = {
        "type": "RECORD",
        "stream": form_name,
        "record": {
            "_form_unique_id": submission.get("id", ""),
            "_read": std_number(
                submission.get("read"),
                default=0.0),
            "_latitude": std_number(
                submission.get("latitude"),
                default=0.0),
            "_longitude": std_number(
                submission.get("longitude"),
                default=0.0),
            "_timestamp": std_date(
                submission.get("timestamp"),
                default="1900-01-01T00:00:00Z"),
            "_user_agent": submission.get("user_agent", ""),
            "_remote_addr": submission.get("remote_addr", "")
        }
    }

    for field in submission["data"]:
        field_type: str = submission["data"][field]["type"]
        if field_type in ["matrix"]:
            write_records__matrix(record, submission["data"][field])
        elif field_type in ["checkbox"]:
            write_records__checkbox(record, submission["data"][field])
        else:
            try:
                field_name: str = submission["data"][field]["label"]
                field_value: str = submission["data"][field]["value"]
                field_flat_value: str = submission["data"][field]["flat_value"]

                if schema_properties[field_name] == _TYPE_STRING:
                    record["record"][field_name] = field_flat_value
                elif schema_properties[field_name] == _TYPE_NUMBER:
                    record["record"][field_name] = std_number(field_value)
                elif schema_properties[field_name] == _TYPE_DATE:
                    record["record"][field_name] = std_date(field_value)
            except UnrecognizedNumber:
                logs.log_error(f"number: [{field_value}]")
            except UnrecognizedDate:
                logs.log_error(f"date:   [{field_value}]")

    return record


def write_records__checkbox(record: JSON, data: JSON) -> None:
    """Handles the assignment of data from a checkbox to the record.
    """

    name: str = data["label"]
    value: Any = data["value"]
    if isinstance(value, str):
        padded_name: str = f"checkbox[{name}][{value}]"
        record["record"][padded_name] = "selected"
    elif isinstance(value, list):
        for inner_name in value:
            padded_name = f"checkbox[{name}][{inner_name}]"
            record["record"][padded_name] = "selected"


def write_records__matrix(record: JSON, data: JSON) -> None:
    """Handles the assignment of data from a matrix to the record.
    """

    name: str = data["label"]
    value: Any = data["value"]
    if isinstance(value, str):
        padded_name: str = f"matrix[{name}][{value}]"
        record["record"][padded_name] = value
    elif isinstance(value, dict):
        for inner_name in value:
            padded_name = f"matrix[{name}][{inner_name}]"
            record["record"][padded_name] = value[inner_name]


def std_text(text: str) -> str:
    """Returns a CDN compliant text.
    """

    # log the received value
    logs.log_conversions(f"text [{text}]")

    # decay to string if not string yet
    text = str(text)

    # always lowercase
    new_text: str = text.lower()

    # no accent marks
    to_replace = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )

    for old_char, new_char in to_replace:
        new_text = new_text.replace(old_char, new_char)

    # just letters and spaces
    new_text = re.sub(r"[^a-z ]", r"", new_text)

    # log the returned value
    logs.log_conversions(f"     [{new_text}]")

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


def std_number(number: Any, **kwargs: Any) -> float:
    """Manipulates a number to provide JSON schema compatible number.

    Args:
        number: The number to manipulate.
        kwargs["default"]: A default value to use in case of emergency.

    Raises:
        UnrecognizedNumber: When it was impossible to find a conversion.

    Returns:
        A JSON schema compliant number.
    """

    # log the received value
    logs.log_conversions(f"number [{number}]")

    # type null instead of str
    if not isinstance(number, str):
        return 0.0

    # point is the decimal separator
    number = number.replace(",", ".")

    # clean typos
    number = re.sub(r"[^\d\.\+-]", r"", number)

    # seems ok, lets try
    try:
        number = float(number)
    except ValueError:
        if "default" in kwargs:
            number = kwargs["default"]
        else:
            raise UnrecognizedNumber

    # log the returned value
    logs.log_conversions(f"       [{number}]")

    return number


def main():
    """Usual entry point.
    """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--auth',
        required=True,
        help='JSON authentication file',
        type=argparse.FileType('r'))
    parser.add_argument(
        '-c', '--conf',
        required=True,
        help='JSON configuration file',
        type=argparse.FileType('r'))
    args = parser.parse_args()

    tap_conf = json.load(args.conf)
    api_token = json.load(args.auth).get("token")

    # get the available forms in the account
    available_forms = get_available_forms(api_token)

    # forms after merge
    real_forms = set()

    for form_name, form_id in available_forms.items():
        # first download, it won't download encrypted/archived forms
        if form_name in tap_conf.get("alias", []):
            alias = tap_conf["alias"].get(form_name)
            write_queries(api_token, alias, form_id)
            real_forms.add(alias)
        else:
            write_queries(api_token, form_name, form_id)
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
