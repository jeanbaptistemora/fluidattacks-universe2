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

# stru_type aliases that improve clarity
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

IS_NONE = lambda stru: stru is None
IS_STR = lambda stru: isinstance(stru, str)
IS_INT = lambda stru: isinstance(stru, int)
IS_BOOL = lambda stru: isinstance(stru, bool)
IS_FLOAT = lambda stru: isinstance(stru, float)
IS_LIST = lambda stru: isinstance(stru, list)
IS_DICT = lambda stru: isinstance(stru, dict)
IS_PRIM = lambda stru: any((f(stru) for f in (IS_STR, IS_INT, IS_BOOL, IS_FLOAT)))
IS_STRU = lambda stru: any((f(stru) for f in (IS_NONE, IS_PRIM, IS_LIST, IS_DICT)))
IS_TIME = lambda stru: (IS_INT(stru) or IS_FLOAT(stru)) and 946684800 < stru < 2524608000
CLEANIT = lambda string: re.sub(r"[^ _a-zA-Z0-9]", "", string)
TYPE = lambda stru: type(stru).__name__ if IS_NONE(to_date(stru)) else "datetime"
CAST = lambda stru: stru if IS_NONE(to_date(stru)) else to_date(stru)


def to_date(date_time: Any) -> Any:
    """Manipulates a date to provide a RFC339 compatible date.
    """

    if ENABLE_TIMESTAMPS and IS_TIME(date_time):
        try:
            date_stru = datetime.datetime.utcfromtimestamp(date_time)
            date_time = date_stru.strftime("%Y-%m-%dT%H:%M:%SZ")
            return date_time
        except ValueError:
            pass

    if IS_STR(date_time):
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


def pt2st(pstru_type: str) -> JSON:
    """Returns a singer stru_type for the python stru_type.
    """

    if pstru_type == "bool":
        return {"stru_type": "boolean"}
    if pstru_type == "float":
        return {"stru_type": "number"}
    if pstru_type == "int":
        return {"stru_type": "integer"}
    if pstru_type == "str":
        return {"stru_type": "string"}
    if pstru_type == "datetime":
        return {"stru_type": "string", "format": "date-time"}
    raise Exception(f"pt2st(pstru_type): pstru_type={pstru_type} not matched")


def prepare_env():
    """Creates/restablish the target folders.
    """

    for _dir in (RECORDS_DIR, SCHEMAS_DIR):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        else:
            for file in os.listdir(_dir):
                os.remove(f"{_dir}/{file}")


def clean_env():
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


def linearize(table_name, structura):
    """ breaks a structura into flat records.
        records are suitable for use into a relational database structure """

    def simplify(stru):
        """ applies CLEANIT to every key in the structura
            removes unsuported data types
            denests every dict of dict to a compound dict """

        if IS_PRIM(stru):
            return stru
        if IS_LIST(stru):
            return list(map(simplify, list(filter(IS_STRU, stru))))
        if IS_DICT(stru):
            new_stru = dict()
            for key, val in stru.items():
                if IS_DICT(val):
                    for nkey, nval in val.items():
                        if IS_STRU(nval):
                            new_stru[f"{CLEANIT(key)}{FIELD_SEP}{CLEANIT(nkey)}"] = nval
                    new_stru = simplify(new_stru)
                elif IS_STRU(val):
                    new_stru[CLEANIT(key)] = simplify(val)
            return new_stru
        return None

    def deconstruct(table="", stru=None, ids=None):
        """ breaks a structura into records of a relational database structure """

        if IS_PRIM(stru):
            deconstruct(table=table, stru=[stru], ids=ids)
        elif IS_LIST(stru):
            for nstru in stru:
                mstru = nstru if IS_DICT(nstru) else {"val": nstru}
                for lvl, this_id in zip(range(len(ids)), ids):
                    mstru[f"sid{lvl}"] = this_id
                deconstruct(table=table, ids=ids, stru=mstru)
        elif IS_DICT(stru):
            record = {}
            for nkey, nstru in stru.items():
                if IS_PRIM(nstru):
                    record[nkey] = nstru
                elif IS_LIST(nstru):
                    nid = ID.gen()
                    ntable = f"{table}{TABLE_SEP}{nkey}"
                    ntable_ids = [nid] if ids is None else ids + [nid]
                    record[ntable] = nid
                    deconstruct(table=ntable, stru=nstru, ids=ntable_ids)
            write(RECORDS_DIR, table, record, func=dumps)

    deconstruct(table=table_name, stru=simplify(structura))


def catalog():
    """ deduce the schema of the generated tables """

    for table_name in os.listdir(RECORDS_DIR):
        schema = {}
        for structura in read(RECORDS_DIR, table_name, loads):
            for key, val in structura.items():
                vtype = TYPE(val)
                try:
                    if not vtype in schema[key]:
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
    # we need some way to tell the entire module that timestamps should be recognized as dates
    # this is an on-demand feature,
    # because may yield ambiguity with numbers that are not timestamps
    global ENABLE_TIMESTAMPS # pylint: disable=global-statement
    ENABLE_TIMESTAMPS = args.enable_timestamps

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

    # Do the heavy lifting (structura)
    prepare_env()
    for stream_str in input_messages:
        try:
            stream_obj = loads(stream_str)
        except JSONDecodeError:
            # possibly an empty line
            continue
        linearize(stream_obj["stream"], stream_obj["record"])
    catalog()

    # Parse everything to singer
    for table in os.listdir(SCHEMAS_DIR):
        pschema = json_from_file(f"{SCHEMAS_DIR}/{table}")
        sschema = {
            "type": "SCHEMA",
            "stream": table,
            "schema": {
                "properties": {f"{f}_{ft}": pt2st(ft) for f, fts in pschema.items() for ft in fts}
            },
            "key_properties": []
        }
        print(dumps(sschema))

        for precord in read(RECORDS_DIR, table, loads):
            srecord = {
                "type": "RECORD",
                "stream": table,
                "record": {f"{f}_{TYPE(v)}": CAST(v) for f, v in precord.items()}
            }
            print(dumps(srecord))

    clean_env()


if __name__ == "__main__":
    main()
