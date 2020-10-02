"""Singer tap for a generic JSON stream."""

import io
import re
import os
import sys
import argparse
import threading
import contextlib
from io import TextIOWrapper
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor

from json import load, loads, dumps
from json.decoder import JSONDecodeError

from typing import (
    Callable,
    List,
    Any,
    Optional,
)

from dateutil.parser import parse as date_parser
from dateutil.parser._parser import ParserError

# type aliases that improve clarity
JSON = Any
STRU = Any

# Module control pannel
FIELD_SEP: str = "__"
TABLE_SEP: str = "____"
SCHEMAS_DIR: str = "____schemas"
RECORDS_DIR: str = "____records"

ENABLE_TIMESTAMPS: bool = False

DATE_FORMATS: List[str] = [
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
]
LOCK = threading.Lock()


def is_str(stru: STRU) -> bool:
    """Return True if stru is str."""
    return isinstance(stru, str)


def is_int(stru: STRU) -> bool:
    """Return True if stru is int."""
    return isinstance(stru, int)


def is_bool(stru: STRU) -> bool:
    """Return True if stru is bool."""
    return isinstance(stru, bool)


def is_float(stru: STRU) -> bool:
    """Return True if stru is float."""
    return isinstance(stru, float)


def is_list(stru: STRU) -> bool:
    """Return True if stru is list."""
    return isinstance(stru, list)


def is_dict(stru: STRU) -> bool:
    """Return True if stru is dict."""
    return isinstance(stru, dict)


def is_base(stru: STRU) -> bool:
    """Return True if stru is a primitive type."""
    return any((f(stru) for f in (is_str, is_int, is_bool, is_float)))


def is_stru(stru: STRU) -> bool:
    """Return True if stru is a Structura."""
    return any((f(stru) for f in (is_base, is_list, is_dict)))


def is_timestamp(stru: STRU) -> bool:
    """Return True if stru is a valid timestamp."""
    #  946684800 = 2000-01-01T00:00:00Z
    # 2147483647 = 2038-01-19T03:14:07Z
    return (is_int(stru) or is_float(stru)) and 946684800 < stru < 2147483647


def clean_str(stru: str) -> str:
    """Clean unvalid chars from a string."""
    return re.sub(r"[^ _a-zA-Z0-9]", "", stru)


def to_date(date_time: Any) -> Any:
    """Manipulate a date to provide a RFC339 compatible date."""
    if ENABLE_TIMESTAMPS and is_timestamp(date_time):
        with contextlib.suppress(OverflowError, ParserError, TypeError):
            return date_parser(str(date_time)).strftime("%Y-%m-%dT%H:%M:%SZ")

    if is_str(date_time):
        with contextlib.suppress(OverflowError, ParserError, TypeError):
            return date_parser(date_time).strftime("%Y-%m-%dT%H:%M:%SZ")

    return False


def stru_type(stru: STRU) -> str:
    """Return the python type of a Structura."""
    return "datetime" if to_date(stru) else type(stru).__name__


def stru_cast(stru: STRU) -> STRU:
    """Cast a Structura."""
    cast_date = to_date(stru)
    return cast_date if cast_date else stru


def pt2st(ptype: str) -> JSON:
    """Return a corresponding singer type for the provided python type."""
    if ptype == "bool":
        return {"type": "boolean"}
    if ptype == "float":
        return {"type": "number"}
    if ptype == "int":
        return {"type": "integer"}
    if ptype == "str":
        return {"type": "string"}
    if ptype == "datetime":
        return {"type": "string", "format": "date-time"}
    raise Exception(f"pt2st(ptype): ptype={ptype} not matched")


def prepare_env():
    """Create/reset the staging area."""
    for _dir in (RECORDS_DIR, SCHEMAS_DIR):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        else:
            for file in os.listdir(_dir):
                os.remove(f"{_dir}/{file}")


def release_env():
    """Clean the staging area on exit."""
    for _dir in (SCHEMAS_DIR, RECORDS_DIR):
        for file in os.listdir(_dir):
            os.remove(f"{_dir}/{file}")
        os.removedirs(f"{_dir}")


def write(
        directory: str,
        table_name: str,
        stru: STRU,
        func: Callable[[STRU], STRU] = lambda x: x) -> None:
    """Write func(stru) to a file."""
    with open(f"{directory}/{table_name}", "a") as file:
        file.write(func(stru))
        file.write("\n")


def read(
        directory: str,
        table_name: str,
        func: Callable[[STRU], STRU] = lambda x: x) -> Any:
    """Yield func(line) per every line of a file."""
    with open(f"{directory}/{table_name}", "r") as file:
        for line in file:
            with contextlib.suppress(JSONDecodeError):
                yield func(line)


def json_from_file(file_path: str) -> JSON:
    """Load a JSON from a file."""
    with open(file_path, "r") as json_file:
        json_stru = load(json_file)
    return json_stru


def linearize(table_name: str, structura: STRU) -> None:
    """Break a Structura into flat records.

    Produced records are suitable for use into a relational database structure.
    """
    linearize__deconstruct(
        table=table_name,
        stru=linearize__simplify(structura),
        ids=None)


def linearize__simplify(stru: STRU) -> STRU:
    """Simplify a Structura.

    Apply clean_str to every key in the structura.
    Denest every dict of dict to a compound dict.
    Remove unsuported data types.
    """
    if is_base(stru):
        return stru
    if is_list(stru):
        return list(map(linearize__simplify, list(filter(is_stru, stru))))
    if is_dict(stru):
        new_stru = dict()
        for key, val in stru.items():
            if is_dict(val):
                for nkey, nval in val.items():
                    if is_stru(nval):
                        nkey_name = \
                            f"{clean_str(key)}{FIELD_SEP}{clean_str(nkey)}"
                        new_stru[nkey_name] = nval
                new_stru = linearize__simplify(new_stru)
            elif is_stru(val):
                new_stru[clean_str(key)] = linearize__simplify(val)
        return new_stru
    return None


def linearize__deconstruct(
        table: str,
        stru: STRU,
        ids: Any) -> STRU:
    """Break a Structura into records of a relational data-structure."""
    if is_base(stru):
        ids = [] if ids is None else ids
        linearize__deconstruct(table=table, stru=[stru], ids=ids)
    elif is_list(stru):
        len_stru = len(stru)
        for index, nstru in enumerate(stru):
            mstru = nstru if is_dict(nstru) else {"val": nstru}
            for lvl, this_id in enumerate(ids):
                mstru[f"sid{lvl}"] = this_id
                mstru["forward_index"] = index
                mstru["backward_index"] = len_stru - 1 - index
            linearize__deconstruct(table=table, ids=ids, stru=mstru)
    elif is_dict(stru):
        record = {}
        for nkey, nstru in stru.items():
            if is_base(nstru):
                record[nkey] = nstru
            elif is_list(nstru):
                nid = os.urandom(256).hex()
                ntable = f"{table}{TABLE_SEP}{nkey}"
                ntable_ids = [nid] if ids is None else ids + [nid]
                record[ntable] = nid
                linearize__deconstruct(
                    table=ntable, stru=nstru, ids=ntable_ids)
        write(RECORDS_DIR, table, record, func=dumps)


def catalog() -> None:
    """Deduce the schema of the generated tables."""
    for table_name in os.listdir(RECORDS_DIR):
        schema: JSON = {}
        for structura in read(RECORDS_DIR, table_name, loads):
            for key, val in structura.items():
                vtype: str = stru_type(val)
                try:
                    if vtype not in schema[key]:
                        schema[key].append(vtype)
                except KeyError:
                    schema[key] = [vtype]
        write(SCHEMAS_DIR, table_name, schema, dumps)


def dump_schema(table: str, file: Optional[TextIOWrapper] = None) -> None:
    def dump_record(precord: Any) -> None:
        record = dumps({
            "type": "RECORD",
            "stream": table,
            "record":
            {f"{f}_{stru_type(v)}": stru_cast(v)
             for f, v in precord.items()}
        })
        with LOCK:
            if file:
                file.write("{}\r".format(record))
            else:
                print(record)

    pschema = json_from_file(f"{SCHEMAS_DIR}/{table}")
    schema = dumps({
        "type": "SCHEMA",
        "stream": table,
        "schema": {
            "properties": {
                f"{f}_{ft}": pt2st(ft)
                for f, fts in pschema.items() for ft in fts
            }
        },
        "key_properties": []
    })
    schema = "{}\r".format(schema)
    with LOCK:
        if file:
            file.write("{}".format(schema))
        else:
            print(schema)
    with ThreadPoolExecutor(max_workers=cpu_count() * 4) as worker:
        worker.map(dump_record, read(RECORDS_DIR, table, loads))


def main() -> None:
    """Usual entry point."""
    parser = argparse.ArgumentParser(
        description="Dump a JSON stream to a Singer stream.")
    parser.add_argument(
        "--enable-timestamps",
        help="Flag to indicate if timestamps should be casted to dates",
        action="store_true",
        default=False,
        dest="enable_timestamps")
    parser.add_argument(
        "--date-formats",
        help="A string of formats separated by comma, extends RFC3339",
        default="",
        dest="date_formats")
    parser.add_argument(
        "--out",
        help="Dump out to file",
        type=argparse.FileType('a+'),
        required=False,
        dest="out")
    args = parser.parse_args()

    # some dates may come in the form of a timestamp
    # if --enable-timestamps is passed as arguments
    #   anything that complies with is_timestamp() will be casted to date

    # pylint: disable=global-statement
    global ENABLE_TIMESTAMPS
    ENABLE_TIMESTAMPS = args.enable_timestamps

    # add the user date formats, filter empty strings
    DATE_FORMATS.extend(f for f in args.date_formats.split(",") if f)

    # Do the heavy lifting (structura)
    prepare_env()

    def structure(stream: str) -> None:
        with contextlib.suppress(JSONDecodeError):
            stream_stru = loads(stream)
            linearize(stream_stru["stream"], stream_stru["record"])

    with ThreadPoolExecutor(max_workers=cpu_count() * 3) as worker:
        worker.map(structure,
                   io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"))

    catalog()

    # Parse everything to singer
    for schema in os.listdir(SCHEMAS_DIR):
        dump_schema(schema, args.out)

    release_env()


if __name__ == "__main__":
    main()
