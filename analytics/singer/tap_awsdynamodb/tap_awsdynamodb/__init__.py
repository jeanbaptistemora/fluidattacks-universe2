"""Singer tap for Amazon Web Services's DynamoDB.

Documentation:
    https://boto3.amazonaws.com/
        v1/documentation/api/latest/reference/services/dynamodb.html

Examples:
    $ tap-awsdynamodb --help
    $ tap-awsdynamodb [params] | target-anysingertarget

Linters:
    pylint:
        Used always.
        $ python3 -m pylint [path]
    flake8:
        Used always except where it contradicts pylint.
        $ python3 -m flake8 [path]
    mypy:
        Used always.
        $ python3 -m mypy --ignore-missing-imports [path]
"""

import re
import ast
import json
import argparse

from uuid import uuid4 as gen_id
from typing import Iterable, Dict, List, Tuple, Any
from datetime import datetime

import boto3 as amazon_sdk

from . import logs

# Type aliases that improve clarity
JSON = Any
DB_SSSN = Any
DB_CLNT = Any
DB_RSRC = Any

_TYPE = {
    "string": {"type": "string"},
    "number": {"type": "number"},
    "date-time": {"type": "string", "format": "date-time"},

    "set": {"type": "string"},
    "list": {"type": "string"},
    "list<dict>": {"type": "string"},
}


def get_connection(credentials: Dict[str, str]) -> Tuple[DB_CLNT, DB_RSRC]:
    """Creates and access point to DynamoDB.

    Args:
        credentials: Must contain valid credentials.

    Raises:
        botocore.exceptions.ClientError: If the credentials are wrong.

    Returns:
        A tuple with a client and a resource object.
    """

    session: DB_SSSN = amazon_sdk.session.Session(
        aws_access_key_id=credentials["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=credentials["AWS_SECRET_ACCESS_KEY"],
        region_name=credentials["AWS_DEFAULT_REGION"]
    )

    db_client: DB_CLNT = session.client('dynamodb')
    db_resource: DB_RSRC = session.resource('dynamodb')

    return (db_client, db_resource)


def list_tables(db_client: DB_CLNT) -> List[str]:
    """List tables in the account.

    Args:
        db_client: A low-level client representing Amazon DynamoDB.

    Returns:
        A tuple with a client and a resource object.
    """

    # start fetching
    response: JSON = db_client.list_tables()
    tables: List[str] = response["TableNames"]

    while "LastEvaluatedKey" in response:
        response = db_client.list_tables(
            ExclusiveStartTableName=response["LastEvaluatedTableName"],
            Limit=10
        )
        tables.append(response["TableNames"])

    return tables


def write_queries(db_resource: DB_RSRC, table_name: str) -> None:
    """Extract rows from table_name and writes them to a file.

    The reason to dump rows to a file first,
    is that presumably a table may be an infinite stream of rows.

    If we are to load all this information in memory to fast access it,
    we'll end up beeing cost-ineffective.

    Given disk is cheaper than RAM, queries will be written to a file and
    processed iterating over the lines of the file.

    Args:
        db_resource: A resource representing Amazon DynamoDB.
        table_name: The table whose rows will be written.
    """

    def dump_to_file(batch: List[JSON]) -> None:
        """Writes a list of JSON objects to a file.

        Args:
            batch: The list of JSON to dump to a file.
        """
        for obj in batch:
            json_obj: Dict[str, str] = {k: str(v) for k, v in obj.items()}
            logs.log_json_obj(table_name, json_obj)

    # Table object
    table: Any = db_resource.Table(table_name)

    response: JSON = table.scan()
    dump_to_file(response["Items"])
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        dump_to_file(response["Items"])


def discover_schema(db_client: DB_CLNT, table_list: List[str]) -> None:
    """Creates a configuration file based on your DynamoDB account.

    All fields will be initially strings, (DynamoDB has no explicit schema).

    You can manually edit the field types, so this file can be used as input
        for the sync mode.

    Args:
        db_client: A low-level client representing Amazon DynamoDB.
        table_list: Contains the names of the tables.
    """

    schema: JSON = {
        "tables": {}
    }

    for table_name in table_list:
        try:
            file = open(f"{logs.DOMAIN}{table_name}.jsonstream", "r")
        except FileNotFoundError:
            # Given empty tables are not downloaded
            # Then there is no file
            continue

        # ask dynamo for a description of the table
        description: JSON = db_client.describe_table(TableName=table_name)
        pkey_schema: List[JSON] = description["Table"]["KeySchema"]

        schema["tables"][table_name] = {
            "primary-keys": [att["AttributeName"] for att in pkey_schema]
        }

        for line in file:
            json_obj = json.loads(line)
            for field in json_obj:
                schema["tables"][table_name]["schema"][field] = "string"

    print(json.dumps(schema, indent=2))


def write_schema(table_name: str, properties: JSON) -> None:
    """Writes a singer schema for table_name to stdout given its properties.

    Args:
        table_name: The table whose schema will be written.
        properties: Human modified configuration file, see discover_schema().
    """

    schema: JSON = {
        "type": "SCHEMA",
        "stream": table_name,
        "key_properties": properties["primary-keys"],
        "schema": {
            "properties": {}
        }
    }

    for field, field_type in properties["schema"].items():
        schema["schema"]["properties"][field] = _TYPE[field_type]

    logs.log_json_obj(f"{table_name}.stdout", schema)
    logs.stdout_json_obj(schema)


def write_records(table_name, properties):
    """ write all the RECORD messages for a given table to stdout """
    special_fields = set()

    file = open(logs.DOMAIN + table_name + ".json", "r")
    line = file.readline()
    while line:
        json_obj = json.loads(line)

        stdout_json_obj = {
            "type": "RECORD",
            "stream": table_name,
            "record": {}
        }

        for key, val in json_obj.items():
            try:
                kind = properties["schema"].get(key)
                if kind == "string":
                    stdout_json_obj["record"][key] = str(val)
                elif kind == "number":
                    stdout_json_obj["record"][key] = std_number(val)
                elif kind == "date-time":
                    stdout_json_obj["record"][key] = std_date(val)
                elif kind in ["set", "list", "list<dict>"]:
                    identifier = str(gen_id())
                    stdout_json_obj["record"][key] = identifier
                    new_table_name = f"{table_name}___{key}"
                    nested_obj = {
                        "source_id": identifier,
                        "value": val
                    }
                    logs.log_json_obj(new_table_name, nested_obj)
                    special_fields.add((new_table_name, kind))
            except UnrecognizedNumber:
                logs.log_error("number: [" + val + "]")
            except UnrecognizedDate:
                logs.log_error("date:   [" + val + "]")
            except ValueError:
                logs.log_error("ValueError:  [" + val + "]")

        logs.log_json_obj(table_name + ".stdout", stdout_json_obj)
        print(json.dumps(stdout_json_obj))

        line = file.readline()

    return special_fields



def transform_nested_objects(table_name, kind):
    """
        When this tap finds a nested object instead of a value:

            -------example_table-------
              ColumnA   |   ColumnB
                123     | {6, 2, "ejm"}

        Then it replaces the nested object in ColumnB with an identifier (type string)
        It does so because relational databases like redshift don't support nested objects )

            -------example_table-------
              ColumnA   |   ColumnB
                123     | id:A2BE3F42

        And inserts a new table:

            ----example_table___ColumnB----
               Source_ID    |     Values
              id:A2BE3F42   |       6
              id:A2BE3F42   |       2
              id:A2BE3F42   |     "ejm"

        You can later do look ups by JOIN on Source_ID
    """

    # pylint: disable=too-many-locals, too-many-statements

    def type_str(obj):
        """ returns a string with the python type of an object """
        if isinstance(obj, str) and is_date(obj):
            return "datetime"
        return type(obj).__name__

    def is_date(date):
        """ detects if a string can be converted to an RFC3339 date """
        try:
            std_date(date)
            return True
        except UnrecognizedDate:
            pass
        return False

    def map_types(type_str):
        map_types = {
            "str": {"type": "string"},
            "int": {"type": "number"},
            "bool": {"type": "boolean"},
            "float": {"type": "number"},
            "datetime": {"type": "string", "format": "date-time"},
        }
        return map_types[type_str]

    def load_records():
        """ load records from file into memory """

        records = []

        # every line contains
        #   { "source_id": identifier, "value": nested_obj }
        #   where nested_obj is a string representing the object to denest

        with open(f"{logs.DOMAIN}{table_name}.jsonstream", "r") as file:
            line = file.readline()
            while line:
                json_obj = json.loads(line)
                source_id = json_obj["source_id"]
                nested_str = json_obj["value"]
                nested_str = re.sub(r"Decimal\('(\d*\.?\d*)'\)", r"\g<1>", nested_str)
                nested_obj = ast.literal_eval(nested_str)
                records.append((source_id, nested_obj))
                line = file.readline()
        return records

    def base_singer_record(source_id):
        """ returns a base singer record """
        singer_record = {
            "type": "RECORD",
            "stream": table_name,
            "record": {
                "__source_id": source_id
            }
        }
        return singer_record

    def denest_list_schema(records):
        """ linearizes a set or list given its elements are any primitive types """
        properties = set()
        for _, nested_obj in records:
            for elem in nested_obj:
                elem_type = type_str(elem)
                field_name = f"{table_name}__{elem_type}"
                properties.add((field_name, elem_type))
        return {f: map_types(t) for f, t in properties}

    def denest_list_record(source_id, elem):
        """ linearizes a set or list given its elements are any primitive types """
        singer_record = base_singer_record(source_id)
        field_name = f"{table_name}__{type_str(elem)}"
        singer_record["record"][field_name] = elem
        return singer_record

    def denest_list_dict_schema(records):
        """ linearizes a list<dict> given its elements are any primitive types """
        properties = set()
        for _, nested_obj in records:
            for elem in nested_obj:
                for key, val in elem.items():
                    val_type = type_str(val)
                    field_name = f"{key}__{val_type}"
                    properties.add((field_name, val_type))
        return {f: map_types(t) for f, t in properties}

    def denest_list_dict_record(source_id, elem):
        """ linearizes a list<dict> given its elements are any primitive types """
        singer_record = base_singer_record(source_id)
        for key, val in elem.items():
            val_type = type_str(val)
            field_name = f"{key}__{type_str(val)}"
            if val_type == "datetime":
                try:
                    singer_record["record"][field_name] = std_date(val)
                except UnrecognizedDate:
                    pass
            else:
                singer_record["record"][field_name] = val
        return singer_record

    # variables
    records = load_records()

    # schema
    singer_schema = {
        "type": "SCHEMA",
        "stream": table_name,
        "key_properties": [],
        "schema": {
            "properties": {}
        }
    }

    if kind in ["set", "list"]:
        singer_schema["schema"]["properties"] = denest_list_schema(records)
    elif kind in ["list<dict>"]:
        singer_schema["schema"]["properties"] = denest_list_dict_schema(records)

    singer_schema["schema"]["properties"]["__source_id"] = map_types("str")
    logs.log_json_obj(f"{table_name}.stdout", singer_schema)
    logs.stdout_json_obj(singer_schema)

    # records
    for source_id, nested_obj in records:
        for elem in nested_obj:
            if kind in ["set", "list"]:
                singer_record = denest_list_record(source_id, elem)
            elif kind in ["list<dict>"]:
                singer_record = denest_list_dict_record(source_id, elem)
            logs.log_json_obj(f"{table_name}.stdout", singer_record)
            logs.stdout_json_obj(singer_record)


def std_structure(obj):
    """
    turns a graph to a plain text representation
        nodes may be (list, dict, set, or str)
    """

    logs.log_conversions("special [" + str(obj) + "]")

    def simplify(obj):
        """ aux function to do the heavy lifting """
        structure = ""
        if isinstance(obj, (list, set)):
            for elem in obj:
                structure += simplify(elem) + ","
            structure = structure[:-1]
        elif isinstance(obj, dict):
            for key, val in obj.items():
                structure += key + ":" + simplify(val) + "-"
            structure = structure[:-1]
        else:
            obj_str = re.sub(r"(,|-|:)", r"", str(obj))
            structure = obj_str
        return structure

    new_structure = simplify(obj)

    logs.log_conversions("        [" + new_structure + "]")

    return new_structure


def std_date(date):
    """
    returns a json schema compliant date (RFC 3339)

    standard: https://tools.ietf.org/html/rfc3339#section-5.6
    """

    # log it
    logs.log_conversions("date [" + date + "]")

    new_date = ""

    # 2018-12-28 14:03:42.123456
    if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+", date):
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    # 2018-12-28 14:03:42
    elif re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", date):
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    # 2017-11-15
    elif re.match(r"^\d{4}-\d{2}-\d{2}", date):
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    else:
        raise UnrecognizedDate

    new_date = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")

    # log it
    logs.log_conversions("     [" + new_date + "]")

    return new_date


def std_number(number):
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

    # no numeric chars after cleaning
    if not number:
        raise UnrecognizedNumber

    # seems ok, lets try
    try:
        number = float(number)
    except ValueError:
        raise UnrecognizedNumber

    # log it
    logs.log_conversions("       [" + str(number) + "]")

    return number


class UnrecognizedNumber(Exception):
    """ Raised when tap didn't find a conversion """


class UnrecognizedDate(Exception):
    """ Raised when tap didn't find a conversion """


def main():
    """ usual entry point """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--auth',
        help='JSON authentication file',
        dest='auth',
        type=argparse.FileType('r'),
        required=True)
    parser.add_argument(
        '-c', '--conf',
        help='JSON config file',
        dest='conf',
        type=argparse.FileType('r'),
        required=True)
    parser.add_argument(
        '-d', '--disc',
        help='Runs the script in discovery mode (generates a customizable CONF file)',
        dest='discovery_mode',
        action='store_true',
        default=False)
    args = parser.parse_args()

    auth_keys = json.load(args.auth)
    conf_sett = json.load(args.conf)

    # ==== AWS DynamoDB  =======================================================
    # write_schema and write_records don't consume quota
    # table_list and discover_schema consumes negligible quota
    # write_queries consumes quota proportional to the table size
    (db_client, db_resource) = get_connection(auth_keys)

    if args.discovery_mode:
        table_list = list_tables(db_client)

        for table_name in table_list:
            write_queries(db_resource, table_name)

        discover_schema(db_client, table_list)
    else:
        for table_name, properties in conf_sett["tables"].items():
            write_queries(db_resource, table_name)
            try:
                write_schema(table_name, properties)
                special_fields = write_records(table_name, properties)
                for new_table_name, kind in special_fields:
                    transform_nested_objects(new_table_name, kind)
            # empty tables are not downloaded
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    main()
