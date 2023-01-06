from ._logger import (
    set_logger,
)
import contextlib
from dateutil.parser import (
    parse as date_parser,
    ParserError,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
import hashlib
import io
from json import (
    dumps,
    load,
    loads,
)
from json.decoder import (
    JSONDecodeError,
)
import logging
import os
from pathlib import (
    Path,
)
import re
import select
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
    Dict,
    List,
    Optional,
    Union,
)
from typing_extensions import (
    TypeGuard,
)

__version__ = "1.0.0"

unsafe_unwrap(set_logger(__name__, __version__))

LOG = logging.getLogger(__name__)
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
primitives = (
    str,
    int,
    bool,
    float,
)
Primitive = Union[str, int, bool, float]


def emit(msg: str) -> None:
    print(msg)


def is_base(stru: STRU) -> bool:
    return isinstance(stru, primitives)


def is_primitive(stru: STRU) -> TypeGuard[Primitive]:
    return is_base(stru)


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
    # pylint: disable=too-many-return-statements
    """Return the python type of a Structura."""
    if to_date(stru):
        return "datetime"
    if isinstance(stru, bool):
        return bool.__name__
    if isinstance(stru, int):
        if stru in range(-2147483648, 2147483648):
            return int.__name__
        return str.__name__
    if isinstance(stru, float):
        return float.__name__
    if isinstance(stru, str):
        return str.__name__ if stru != "" else "EmptyStr"
    return type(stru).__name__


def stru_cast(stru: STRU, type_ref: str) -> STRU:
    """Cast a Structura."""
    if type_ref == "datetime":
        return to_date(stru)
    if type_ref == "bool":
        return bool(stru)
    if type_ref == "int":
        return int(stru)
    if type_ref == "float":
        return float(stru)
    if type_ref in ("EmptyStr", "str"):
        return str(stru).replace("\n", "")
    raise Exception(f"Not supported type: {type_ref}")


def pt2st(ptype: str) -> JSON:
    """Return a corresponding singer type for the provided python type."""
    if ptype == "bool":
        return {"type": "boolean"}
    if ptype == "float":
        return {"type": "number"}
    if ptype == "int":
        return {"type": "integer"}
    if ptype in ("EmptyStr", "str"):
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
    with open(f"{directory}/{table_name}", "a", encoding="UTF-8") as file:
        file.write(func(stru))
        file.write("\n")


def read(
    directory: str, table_name: str, func: Callable[[STRU], STRU] = lambda x: x
) -> Any:
    """Yield func(line) per every line of a file."""
    with open(f"{directory}/{table_name}", "r", encoding="UTF-8") as file:
        for line in file:
            with contextlib.suppress(JSONDecodeError):
                yield func(line)


def json_from_file(file_path: str) -> JSON:
    """Load a JSON from a file."""
    with open(file_path, "r", encoding="UTF-8") as json_file:
        json_stru = load(json_file)
    return json_stru


def linearize(table_name: str, structura: STRU) -> None:
    """Break a Structura into flat records.

    Produced records are suitable for use into a relational database structure.
    """
    linearize__deconstruct(
        table=table_name, stru=linearize__simplify(structura), ids=None
    )


def linearize__simplify(stru: STRU) -> STRU:  # NOSONAR
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
        new_stru = {}
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


def struct_hash(stru: STRU) -> str:
    hash_id = hashlib.sha256()
    if is_primitive(stru):
        hash_id.update(bytes(str(stru), "utf-8"))
        return hash_id.hexdigest()
    if isinstance(stru, list):
        for item in stru:
            hash_id.update(bytes(struct_hash(item), "utf-8"))
        return hash_id.hexdigest()
    if isinstance(stru, dict):
        for key, val in sorted(stru.items()):
            hash_id.update(bytes(struct_hash(key), "utf-8"))
            hash_id.update(bytes(struct_hash(val), "utf-8"))
        return hash_id.hexdigest()
    raise Exception(f"Unexpected type {type(stru)}")


def nested_id(items: List[Any]) -> str:
    return struct_hash(items)


def linearize__deconstruct(  # NOSONAR
    table: str, stru: STRU, ids: Any
) -> STRU:
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
                nid = nested_id(nstru)
                ntable = f"{table}{TABLE_SEP}{nkey}"
                ntable_ids = [nid] if ids is None else ids + [nid]
                record[ntable] = nid
                linearize__deconstruct(
                    table=ntable, stru=nstru, ids=ntable_ids
                )
        write(RECORDS_DIR, table, record, func=dumps)


def catalog(schema_dir: str) -> None:
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
        write(schema_dir, table_name, schema, dumps)


def choose_type(types: List[str]) -> str:
    priority = [
        "EmptyStr",
        "datetime",
        "bool",
        "int",
        "float",
        "str",
    ]
    return priority[max(map(priority.index, types))]


def dump_schema(table: str, schemas_dir: str) -> None:
    LOG.info("dumping schema: %s", table)
    pschema = json_from_file(f"{schemas_dir}/{table}")
    props = {}
    for key, fts in pschema.items():
        selected_type = choose_type(fts)
        LOG.debug("%s[%s]: %s", key, selected_type, fts)
        props[f"{key}_{selected_type}"] = pt2st(selected_type)
        if "EmptyStr" in fts:
            props[f"{key}_str"] = pt2st("str")
    emit(
        dumps(
            {
                "type": "SCHEMA",
                "stream": table,
                "schema": {"properties": props},
                "key_properties": [],
            }
        )
    )


def emit_record(
    record: Dict[str, STRU], field: str, value: Any, selected_type: str
) -> None:
    if value == "":
        record[f"{field}_str"] = value
    else:
        if selected_type == "EmptyStr":
            record[f"{field}_str"] = stru_cast(value, selected_type)
        else:
            record[f"{field}_{selected_type}"] = stru_cast(
                value, selected_type
            )


def dump_records(table: str, schemas_dir: str) -> None:
    LOG.info("dumping records: %s", table)
    pschema = json_from_file(f"{schemas_dir}/{table}")
    path = Path(RECORDS_DIR) / Path(table)
    if not path.exists():
        return None
    for precord in read(RECORDS_DIR, table, loads):
        record: Dict[str, STRU] = {}
        for field, value in precord.items():
            if field in pschema:
                types = pschema[field]
                selected_type = choose_type(types)
                emit_record(record, field, value, selected_type)
            else:
                LOG.warning(
                    "field `%s` missing in schema of table `%s`", field, table
                )
        emit(
            dumps(
                {
                    "type": "RECORD",
                    "stream": table,
                    "record": record,
                }
            )
        )
    return None


def main(  # NOSONAR
    date_formats: List[str],
    use_cache: bool,
    schema_folder: Optional[str],
    stream_records: bool,
) -> None:
    """Usual entry point."""

    _schemas_dir = schema_folder if schema_folder else SCHEMAS_DIR

    # add the user date formats, filter empty strings
    DATE_FORMATS.extend(date_formats)

    # Do the heavy lifting (structura)
    prepare_env()

    if select.select(
        [
            sys.stdin,
        ],
        [],
        [],
        0.0,
    )[0]:
        LOG.info("Processing stream...")
        for stream in io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"):
            LOG.info("stream: %s", stream)
            with contextlib.suppress(JSONDecodeError):
                stream_stru = loads(stream)
                _type = stream_stru.get("type")
                if _type is None or _type == "RECORD":
                    linearize(stream_stru["stream"], stream_stru["record"])
                elif _type == "STATE":
                    write(STATE_DIR, "states", stream)
    else:
        LOG.warning("No input")
    if not use_cache:
        catalog(_schemas_dir)

    # Parse everything to singer
    LOG.info("to singer transform...")
    for schema in os.listdir(_schemas_dir):
        dump_schema(schema, _schemas_dir)
        if stream_records:
            dump_records(schema, _schemas_dir)
    if os.path.exists(f"{STATE_DIR}/states"):
        for state in read(STATE_DIR, "states"):
            if state.rstrip():
                print(state.rstrip())

    release_env()
