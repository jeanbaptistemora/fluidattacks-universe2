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
