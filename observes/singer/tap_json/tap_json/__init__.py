"""Singer tap for a generic JSON stream."""

import contextlib
from dateutil.parser import (
    parse as date_parser,
)
from dateutil.parser._parser import (
    ParserError,
)
import io
from json import (
    dumps,
    load,
    loads,
)
from json.decoder import (
    JSONDecodeError,
)
import os
import re
import sys
from tap_json.env import (
    prepare_env,
    RECORDS_DIR,
    release_env,
    SCHEMAS_DIR,
    STATE_DIR,
)
from typing import (
    Any,
    Callable,
    List,
)

# type aliases that improve clarity
JSON = Any
STRU = Any

# Module control pannel
FIELD_SEP: str = "__"
TABLE_SEP: str = "____"
ENABLE_TIMESTAMPS: bool = False

DATE_FORMATS: List[str] = [
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
]


def emit(msg: str) -> None:
    print(msg)


def is_base(stru: STRU) -> bool:
    primitives = (
        str,
        int,
        bool,
        float,
    )
    return isinstance(stru, primitives)


def is_stru(stru: STRU) -> bool:
    """Return True if stru is a Structura."""
    return is_base(stru) or isinstance(stru, (list, dict))


def is_timestamp(stru: STRU) -> bool:
    """Return True if stru is a valid timestamp."""
    #  946684800 = 2000-01-01T00:00:00Z
    # 2147483647 = 2038-01-19T03:14:07Z
    return isinstance(stru, (int, float)) and 946684800 < stru < 2147483647


def clean_str(stru: str) -> str:
    """Clean unvalid chars from a string."""
    return re.sub(r"[^ _a-zA-Z0-9]", "", stru)


def to_date(date_time: Any) -> Any:
    """Manipulate a date to provide a RFC339 compatible date."""
    if ENABLE_TIMESTAMPS and is_timestamp(date_time):
        with contextlib.suppress(OverflowError, ParserError, TypeError):
            return date_parser(str(date_time)).strftime("%Y-%m-%dT%H:%M:%SZ")

    if isinstance(date_time, str):
        with contextlib.suppress(OverflowError, ParserError, TypeError):
            try:
                float(date_time)
            except ValueError:
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


def write(
    directory: str,
    table_name: str,
    stru: STRU,
    func: Callable[[STRU], STRU] = lambda x: x,
) -> None:
    """Write func(stru) to a file."""
    with open(f"{directory}/{table_name}", "a") as file:
        file.write(func(stru))
        file.write("\n")


def read(
    directory: str, table_name: str, func: Callable[[STRU], STRU] = lambda x: x
) -> Any:
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
        table=table_name, stru=linearize__simplify(structura), ids=None
    )


def linearize__simplify(stru: STRU) -> STRU:
    """Simplify a Structura.

    Apply clean_str to every key in the structura.
    Denest every dict of dict to a compound dict.
    Remove unsuported data types.
    """
    if is_base(stru):
        return stru
    if isinstance(stru, list):
        return list(map(linearize__simplify, list(filter(is_stru, stru))))
    if isinstance(stru, dict):
        new_stru = dict()
        for key, val in stru.items():
            if isinstance(val, dict):
                for nkey, nval in val.items():
                    if is_stru(nval):
                        nkey_name = (
                            f"{clean_str(key)}{FIELD_SEP}{clean_str(nkey)}"
                        )
                        new_stru[nkey_name] = nval
                new_stru = linearize__simplify(new_stru)
            elif is_stru(val):
                new_stru[clean_str(key)] = linearize__simplify(val)
        return new_stru
    return None


def linearize__deconstruct(table: str, stru: STRU, ids: Any) -> STRU:
    """Break a Structura into records of a relational data-structure."""
    if is_base(stru):
        ids = [] if ids is None else ids
        linearize__deconstruct(table=table, stru=[stru], ids=ids)
    elif isinstance(stru, list):
        len_stru = len(stru)
        for index, nstru in enumerate(stru):
            mstru = nstru if isinstance(nstru, dict) else {"val": nstru}
            for lvl, this_id in enumerate(ids):
                mstru[f"sid{lvl}"] = this_id
                mstru["forward_index"] = index
                mstru["backward_index"] = len_stru - 1 - index
            linearize__deconstruct(table=table, ids=ids, stru=mstru)
    elif isinstance(stru, dict):
        record = {}
        for nkey, nstru in stru.items():
            if is_base(nstru):
                record[nkey] = nstru
            elif isinstance(nstru, list):
                nid = os.urandom(256).hex()
                ntable = f"{table}{TABLE_SEP}{nkey}"
                ntable_ids = [nid] if ids is None else ids + [nid]
                record[ntable] = nid
                linearize__deconstruct(
                    table=ntable, stru=nstru, ids=ntable_ids
                )
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


def dump_schema(table: str) -> None:
    pschema = json_from_file(f"{SCHEMAS_DIR}/{table}")
    emit(
        dumps(
            {
                "type": "SCHEMA",
                "stream": table,
                "schema": {
                    "properties": {
                        f"{f}_{ft}": pt2st(ft)
                        for f, fts in pschema.items()
                        for ft in fts
                    }
                },
                "key_properties": [],
            }
        )
    )

    for precord in read(RECORDS_DIR, table, loads):
        emit(
            dumps(
                {
                    "type": "RECORD",
                    "stream": table,
                    "record": {
                        f"{f}_{stru_type(v)}": stru_cast(v)
                        for f, v in precord.items()
                    },
                }
            )
        )


def main(date_formats: List[str]) -> None:
    """Usual entry point."""

    # add the user date formats, filter empty strings
    DATE_FORMATS.extend(date_formats)

    # Do the heavy lifting (structura)
    prepare_env()

    for stream in io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"):
        with contextlib.suppress(JSONDecodeError):
            stream_stru = loads(stream)
            _type = stream_stru.get("type")
            if _type is None or _type == "RECORD":
                linearize(stream_stru["stream"], stream_stru["record"])
            elif _type == "STATE":
                write(STATE_DIR, "states", stream)
    catalog()

    # Parse everything to singer
    for schema in os.listdir(SCHEMAS_DIR):
        dump_schema(schema)
    if os.path.exists(f"{STATE_DIR}/states"):
        for state in read(STATE_DIR, "states"):
            if state.rstrip():
                print(state.rstrip())

    release_env()
