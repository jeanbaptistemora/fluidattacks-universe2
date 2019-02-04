"""Singer tap for a JSON stream.
"""

import io
import re
import os
import sys
import datetime
import argparse

from json import load, loads, dumps
from json.decoder import JSONDecodeError

from typing import Callable, Tuple, Any

# type aliases that improve clarity
JSON = Any
STRU = Any

# Module control pannel
FIELD_SEP: str = "__"
TABLE_SEP: str = "____"
SCHEMAS_DIR: str = "____schemas"
RECORDS_DIR: str = "____records"

ENABLE_TIMESTAMPS: bool = False

DATE_FORMATS: Tuple[str, str, str, str, str, str, str] = (
    "%Y %m %d %H %M %S %f",
    "%Y %m %d %H %M %S",
    "%Y %m %d",
    "%d %m %Y",
    "%b %d %Y",
    "%b %Y",
    "%H %M",
)


class GenID():
    """Class to generate light weight unique ids.
    """

    def __init__(self) -> None:
        self.identifier: int = 0

    def __repr__(self) -> str:
        return format(self.identifier, "X")

    def seed(self, seed: int) -> None:
        """Seeds the generator.
        """

        self.identifier = seed

    def gen(self) -> str:
        """Generates a unique id.
        """

        self.identifier += 1
        return repr(self)


ID: GenID = GenID()


def is_str(stru: STRU) -> bool:
    """Returns True if stru is str.
    """

    return isinstance(stru, str)


def is_int(stru: STRU) -> bool:
    """Returns True if stru is int.
    """

    return isinstance(stru, int)


def is_bool(stru: STRU) -> bool:
    """Returns True if stru is bool.
    """

    return isinstance(stru, bool)


def is_float(stru: STRU) -> bool:
    """Returns True if stru is float.
    """

    return isinstance(stru, float)


def is_list(stru: STRU) -> bool:
    """Returns True if stru is list.
    """

    return isinstance(stru, list)


def is_dict(stru: STRU) -> bool:
    """Returns True if stru is dict.
    """

    return isinstance(stru, dict)


def is_base(stru: STRU) -> bool:
    """Returns True if stru is a primitive type.
    """

    return any((f(stru) for f in (is_str, is_int, is_bool, is_float)))


def is_stru(stru: STRU) -> bool:
    """Returns True if stru is a Structura.
    """

    return any((f(stru) for f in (is_base, is_list, is_dict)))


def is_timestamp(stru: STRU) -> bool:
    """Returns True if stru is a valid timestamp.
    """

    return (is_int(stru) or is_float(stru)) and 946684800 < stru < 2147483647


def clean_str(stru: str) -> str:
    """Cleans unvalid chars from a string.
    """

    return re.sub(r"[^ _a-zA-Z0-9]", "", stru)


def to_date(date_time: Any) -> Any:
    """Manipulates a date to provide a RFC339 compatible date.
    """

    if ENABLE_TIMESTAMPS and is_timestamp(date_time):
        try:
            date_stru = datetime.datetime.utcfromtimestamp(date_time)
            date_time = date_stru.strftime("%Y-%m-%dT%H:%M:%SZ")
            return date_time
        except ValueError:
            pass

    if is_str(date_time):
        date_time = re.sub(r"[^\d]", r" ", date_time)
        date_time = re.sub(r"\s+", r" ", date_time)

        for date_format in DATE_FORMATS:
            try:
                date_stru = datetime.datetime.strptime(date_time, date_format)
                date_time = date_stru.strftime("%Y-%m-%dT%H:%M:%SZ")
                return date_time
            except ValueError:
                pass

    return False


def stru_type(stru: STRU) -> str:
    """Returns the python type of a Structura.
    """

    return "datetime" if to_date(stru) else type(stru).__name__


def stru_cast(stru: STRU) -> STRU:
    """Casts a stru.
    """

    cast_date = to_date(stru)
    return cast_date if cast_date else stru


def pt2st(ptype: str) -> JSON:
    """Returns a singer type for the python type.
    """

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
    """Creates/restablish the target folders.
    """

    for _dir in (RECORDS_DIR, SCHEMAS_DIR):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        else:
            for file in os.listdir(_dir):
                os.remove(f"{_dir}/{file}")


def release_env():
    """Cleans the used paths on exit.
    """

    for _dir in (SCHEMAS_DIR, RECORDS_DIR):
        for file in os.listdir(_dir):
            os.remove(f"{_dir}/{file}")
        os.removedirs(f"{_dir}")


def write(
        directory: str,
        table_name: str,
        stru: STRU,
        func: Callable[[STRU], STRU] = lambda x: x) -> None:
    """Writes func(stru) to a file.
    """

    with open(f"{directory}/{table_name}", "a") as file:
        file.write(func(stru))
        file.write("\n")


def read(
        directory: str,
        table_name: str,
        func: Callable[[STRU], STRU] = lambda x: x) -> Any:
    """Yields func(line) per every line of a file.
    """

    with open(f"{directory}/{table_name}", "r") as file:
        for line in file:
            yield func(line)


def json_from_file(file_path: str) -> JSON:
    """Loads a json from a file.
    """

    with open(file_path, "r") as json_file:
        json_stru = load(json_file)
    return json_stru


def linearize(table_name: str, structura: STRU) -> None:
    """Breaks a structura into flat records.

    Produced records are suitable for use into a relational database structure.
    """

    linearize__deconstruct(
        table=table_name,
        stru=linearize__simplify(structura),
        ids=None)


def linearize__simplify(stru: STRU) -> STRU:
    """Simplifies a Structura.

    Applies clean_str to every key in the structura.
    Denests every dict of dict to a compound dict.
    Removes unsuported data types.
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
    """Breaks a structura into records of a relational data-structure.
    """

    if is_base(stru):
        ids = [] if ids is None else ids
        linearize__deconstruct(table=table, stru=[stru], ids=ids)
    elif is_list(stru):
        for nstru in stru:
            mstru = nstru if is_dict(nstru) else {"val": nstru}
            for lvl, this_id in enumerate(ids):
                mstru[f"sid{lvl}"] = this_id
            linearize__deconstruct(table=table, ids=ids, stru=mstru)
    elif is_dict(stru):
        record = {}
        for nkey, nstru in stru.items():
            if is_base(nstru):
                record[nkey] = nstru
            elif is_list(nstru):
                nid = ID.gen()
                ntable = f"{table}{TABLE_SEP}{nkey}"
                ntable_ids = [nid] if ids is None else ids + [nid]
                record[ntable] = nid
                linearize__deconstruct(
                    table=ntable, stru=nstru, ids=ntable_ids)
        write(RECORDS_DIR, table, record, func=dumps)


def catalog() -> None:
    """Deduce the schema of the generated tables.
    """

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


def main():
    """ usual entry point """

    parser = argparse.ArgumentParser(
        description=" dumps a JSON stream to a Singer stream ")
    parser.add_argument(
        "--enable-timestamps",
        help="JSON authentication file",
        action="store_true",
        default=False,
        dest="enable_timestamps")
    args = parser.parse_args()

    # some dates may come in the form of a timestamp
    # if --enable-timestamps is passed as arguments
    #   anything that complies with is_timestamp() will be casted to date

    # pylint: disable=global-statement
    global ENABLE_TIMESTAMPS
    ENABLE_TIMESTAMPS = args.enable_timestamps

    # Do the heavy lifting (structura)
    prepare_env()
    for stream_str in io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"):
        try:
            stream_stru = loads(stream_str)
        except JSONDecodeError:
            # possibly an empty line
            continue
        linearize(stream_stru["stream"], stream_stru["record"])
    catalog()

    # Parse everything to singer
    for table in os.listdir(SCHEMAS_DIR):
        pschema = json_from_file(f"{SCHEMAS_DIR}/{table}")
        sschema = {
            "type": "SCHEMA",
            "stream": table,
            "schema": {
                "properties": {
                    f"{f}_{ft}": pt2st(ft)
                    for f, fts in pschema.items()
                    for ft in fts
                }
            },
            "key_properties": []
        }
        print(dumps(sschema))

        for precord in read(RECORDS_DIR, table, loads):
            srecord = {
                "type": "RECORD",
                "stream": table,
                "record": {
                    f"{f}_{stru_type(v)}": stru_cast(v)
                    for f, v in precord.items()
                }
            }
            print(dumps(srecord))

    release_env()


if __name__ == "__main__":
    main()
