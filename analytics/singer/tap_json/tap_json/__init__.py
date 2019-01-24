""" Singer tap for a JSON stream """

import io
import re
import os
import sys
import argparse

from json import load, loads, dumps
from datetime import datetime

class ID():
    """ class to generate light weight unique ids """
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.identifier = 0
    def get(self):
        """ generates a unique id """
        self.identifier += 1
        return format(self.identifier, "X")

_FSEP = "__"           # field separator
_TSEP = "____"         # table separator
_SDIR = "____schemas"  # schemas directory
_RDIR = "____records"  # records directory

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

ID_GEN = ID()

ENABLE_TS = False
DATE_FORMATS = (
    "%Y %m %d %H %M %S %f",
    "%Y %m %d %H %M %S",
    "%Y %m %d",
)

def to_date(date_time):
    """ tries to match the date with the provided DATE_FORMATS
        returns a RFC3339 date if it finds a match """

    if ENABLE_TS and IS_TIME(date_time):
        try:
            date_obj = datetime.utcfromtimestamp(date_time)
            date_time = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
            return date_time
        except ValueError:
            pass

    if IS_STR(date_time):
        date_time = re.sub(r"[^\d]", " ", date_time)
        date_time = re.sub(r"\s+", " ", date_time)

        for date_format in DATE_FORMATS:
            try:
                date_obj = datetime.strptime(date_time, date_format)
                date_time = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
                return date_time
            except ValueError:
                pass

    return None

def pt2st(ptype):
    """ returns a singer type for the python type """
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
    """ creates/restablish the target folder """

    for _dir in (_RDIR, _SDIR):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        else:
            for file in os.listdir(_dir):
                os.remove(f"{_dir}/{file}")

def clean_env():
    """ cleans the used paths on exit """
    for _dir in (_SDIR, _RDIR):
        for file in os.listdir(_dir):
            os.remove(f"{_dir}/{file}")
        os.removedirs(f"{_dir}")

def write(directory, table_name, obj, func=lambda x: x):
    """ writes func(obj) to a file"""

    with open(f"{directory}/{table_name}", "a") as file:
        file.write(func(obj))
        file.write("\n")

def read(directory, table_name, func=lambda x: x):
    """ iterator to func(line) of file """

    with open(f"{directory}/{table_name}", "r") as file:
        line = file.readline()
        while line:
            yield func(line)
            line = file.readline()

def json_from_file(file_path):
    """ loads a json from a file """
    with open(file_path, "r") as json_file:
        json_obj = load(json_file)
    return json_obj

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
                            new_stru[f"{CLEANIT(key)}{_FSEP}{CLEANIT(nkey)}"] = nval
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
                    nid = ID_GEN.get()
                    ntable = f"{table}{_TSEP}{nkey}"
                    ntable_ids = [nid] if ids is None else ids + [nid]
                    record[ntable] = nid
                    deconstruct(table=ntable, stru=nstru, ids=ntable_ids)
            write(_RDIR, table, record, func=dumps)

    deconstruct(table=table_name, stru=simplify(structura))

def catalog():
    """ deduce the schema of the generated tables """

    for table_name in os.listdir(_RDIR):
        schema = {}
        for structura in read(_RDIR, table_name, loads):
            for key, val in structura.items():
                vtype = TYPE(val)
                try:
                    if not vtype in schema[key]:
                        schema[key].append(vtype)
                except KeyError:
                    schema[key] = [vtype]
        write(_SDIR, table_name, schema, dumps)

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
    global ENABLE_TS # pylint: disable=global-statement
    ENABLE_TS = args.enable_timestamps

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

    # Do the heavy lifting (structura)
    prepare_env()
    for stream_str in input_messages:
        stream_obj = loads(stream_str)
        linearize(stream_obj["stream"], stream_obj["record"])
    catalog()

    # Parse everything to singer
    for table in os.listdir(_SDIR):
        pschema = json_from_file(f"{_SDIR}/{table}")
        sschema = {
            "type": "SCHEMA",
            "stream": table,
            "schema": {
                "properties": {f"{f}_{ft}": pt2st(ft) for f, fts in pschema.items() for ft in fts}
            },
            "key_properties": []
        }
        print(dumps(sschema))

        for precord in read(_RDIR, table, loads):
            srecord = {
                "type": "RECORD",
                "stream": table,
                "record": {f"{f}_{TYPE(v)}": CAST(v) for f, v in precord.items()}
            }
            print(dumps(srecord))

    clean_env()

if __name__ == "__main__":
    main()
