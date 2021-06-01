import argparse
from contextlib import (
    contextmanager,
)
import datetime
import json
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
)
import sys
from tap_mixpanel.api import (
    ApiClient,
    Credentials,
)
from typing import (
    Any,
    Dict,
    IO,
    Iterator,
    List,
    Tuple,
)


@contextmanager
def open_temp(file: IO[str]) -> Iterator[IO[str]]:
    try:
        file.seek(0)
        yield file
    finally:
        file.flush()


def read_properties(schema_file: str) -> Dict[str, Any]:
    with open(schema_file) as cred:
        credentials = json.loads(cred.read())
    return dict(credentials)


def config_completion(conf: Dict[str, str]) -> Dict[str, str]:
    to_date = datetime.date.today().strftime("%Y-%m-%d")
    from_date = datetime.date.today() - datetime.timedelta(days=365)
    conf["from_date"] = str(from_date)
    conf["to_date"] = to_date
    return conf


def handle_t_f(raw_str: str) -> str:
    t_f_formatted = raw_str.replace("false", '"false"')
    t_f_formatted = t_f_formatted.replace("true", "'true'")
    t_f_formatted = t_f_formatted.replace("null", "'null'")
    return t_f_formatted


def handle_null(dct: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(dct["properties"].keys())
    for key in keys:
        if dct["properties"][key] == "null":
            del dct["properties"][key]
        else:
            continue
    return dct


def new_formatted_data(formatted_data: List[Dict]) -> List[Dict]:
    format_def = []
    for entry in formatted_data:
        if entry:
            entry["properties"]["event"] = entry["event"]
            format_def.append(entry["properties"])
        else:
            continue
    return format_def


def take_dtypes(data: List[Dict[str, Any]]) -> Dict[str, str]:
    def parsing_dtype(obs: Any) -> Any:
        result = None
        if isinstance(obs, int) and len(str(obs)) == 10:
            result = "date-time"
        elif isinstance(obs, str):
            result = "string"
        elif isinstance(obs, (int, float)):
            result = "number"
        return result

    dtypes = {}
    for dct in data:
        for reg in dct:
            dtypes[reg] = parsing_dtype(dct[reg])
    return dtypes


def date_parser(date_number: int) -> str:
    date_formated = datetime.datetime.fromtimestamp(date_number).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return date_formated


def check_and_parse(
    sample: Dict[str, Any], dtypes: Dict[str, str]
) -> List[Tuple[str, Any]]:
    output = []
    for i in dtypes:
        try:
            if dtypes[i] == "date-time":
                if isinstance(sample[i], datetime.datetime):
                    output.append((i, sample[i]))
                elif isinstance(sample[i], int):
                    output.append((i, date_parser(sample[i])))
            else:
                output.append((i, sample[i]))
        except (ValueError, KeyError):
            continue
    return output


def write_file(singer_schema: str, singer_records: List[str]) -> None:
    with open("Events.txt", "w+") as stream_file:
        str_records = "\n".join(singer_records)
        str_stream = str(singer_schema) + "\n" + str_records
        stream_file.write(str_stream)


def lowercase_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for key, value in data.items():
        result[key.lower()] = value
    return result


def process_line(line: str) -> Dict[str, Any]:
    data: Dict[str, Any] = json.loads(line)
    data = handle_null(data)
    data = new_formatted_data([data])[0]
    dtypes = take_dtypes([data])
    data = dict(check_and_parse(data, dtypes))
    data = lowercase_keys(data)
    return data


def format_and_emit_data(data_file: IO[str]) -> None:
    with open_temp(data_file) as tmp:
        line = tmp.readline()
        while line:
            record = SingerRecord(stream="Events", record=process_line(line))
            factory.emit(record)
            line = tmp.readline()


def main() -> None:
    # Entry Point
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--auth",
        action="store",
        help="config file containing mixpanel credentials",
    )
    parser.add_argument(
        "-c",
        "--conf",
        action="store",
        help="file containing the table properties",
    )
    args = parser.parse_args()
    auth_file = args.auth
    conf_file = args.conf
    raw_creds = read_properties(auth_file)
    client = ApiClient.from_creds(Credentials.from_json(raw_creds))
    raw_date_range = config_completion({})
    date_range = (raw_date_range["from_date"], raw_date_range["to_date"])
    tables = read_properties(conf_file)["tables"]

    for table in tables:
        print(table, file=sys.stderr)
        with client.data_handler(table, date_range) as raw_data_file:
            format_and_emit_data(raw_data_file)


if __name__ == "__main__":
    main()
