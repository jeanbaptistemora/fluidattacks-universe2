import json
import datetime
import ast
import sys
import argparse
from typing import List, Dict, Tuple, Any
import requests


def read_properties(schema_file: str) -> Dict[str, Any]:
    with open(schema_file) as cred:
        credentials = json.loads(cred.read())
    return dict(credentials)


def config_completion(conf: Dict[str, str]) -> Dict[str, str]:
    to_date = datetime.date.today().strftime("%Y-%m-%d")
    from_date = datetime.date.today() - datetime.timedelta(days=365)
    conf['from_date'] = str(from_date)
    conf['to_date'] = to_date
    return conf


def handle_t_f(raw_str: str) -> str:
    t_f_formatted = raw_str.replace('false', '"false"')
    t_f_formatted = t_f_formatted.replace('true', "'true'")
    t_f_formatted = t_f_formatted.replace('null', "'null'")
    return t_f_formatted


def handle_null(dct: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(dct['properties'].keys())
    for key in keys:
        if dct['properties'][key] == 'null':
            del dct['properties'][key]
        else:
            continue
    return dct


def load_data(event: str, credentials: Dict[str, Any]) -> List[Dict]:
    from_date = credentials['from_date']
    to_date = credentials['to_date']
    parameters = {"from_date": from_date, "to_date": to_date,
                  "event": f'["{event}"]'}
    authorization = (credentials['API_secret'], credentials['token'])
    result = requests.get("https://data.mixpanel.com/api/2.0/export/",
                          auth=authorization, params=parameters)
    data = raw_to_formated(result.text)
    return data


def raw_to_formated(raw_data: str) -> List[Dict]:
    interm = raw_data.split('\n')
    data = [
        ast.literal_eval(handle_t_f(dct))
        for dct in interm
        if dct
    ]
    return data


def new_formatted_data(formatted_data: List[Dict]) -> List[Dict]:
    format_def = []
    for entry in formatted_data:
        if entry:
            entry['properties']['event'] = entry['event']
            format_def.append(entry['properties'])
        else:
            continue
    return format_def


def take_dtypes(data: List[Dict]) -> Dict[str, str]:
    def parsing_dtype(obs: Any) -> Any:
        result = None
        if isinstance(obs, int) and len(str(obs)) == 10:
            result = 'date-time'
        elif isinstance(obs, str):
            result = 'string'
        elif isinstance(obs, (int, float)):
            result = 'number'
        return result

    dtypes = {}
    for dct in data:
        for reg in dct:
            dtypes[reg] = parsing_dtype(dct[reg])
    return dtypes


def date_parser(date_number: int) -> str:
    date_formated = datetime.datetime.fromtimestamp(date_number)\
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    return date_formated


def check_and_parse(sample: Dict[str, Any],
                    dtypes: Dict[str, str]) -> List[Tuple[str, Any]]:
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


def schema_parser(dtypes: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    primary_key = ["$insert_id"]
    singer_schema = {"type": "SCHEMA", "stream": "Events",
                     "key_properties": primary_key, "schema": dtypes}
    return singer_schema


def generate_singer_schema(schema: Dict[str, Any]) -> str:
    schema_base = {key: ({"type": value} if value != "date-time"
                         else {"type": "string", "format": "date-time"})
                   for (key, value) in schema.items()}
    schema_base = {"properties": schema_base}
    singer_schema = json.dumps(schema_parser(schema_base))
    return singer_schema


def record_parser(record_dict: Dict[str, Any]) -> str:
    singer_record = json.dumps({"type": "RECORD",
                                "stream": "Events", "record": record_dict})
    return str(singer_record)


def generate_singer_records(data: List[Dict],
                            dtypes: Dict[str, str]) -> List[str]:
    itr_records = [check_and_parse(sample, dtypes) for sample in data]
    std_records = [dict(std_tuple) for std_tuple in itr_records]
    singer_records = [record_parser(dct) for dct in std_records]
    return singer_records


def write_file(singer_schema: str, singer_records: List[str]) -> None:
    with open("Events.txt", 'w+') as stream_file:
        str_records = "\n".join(singer_records)
        str_stream = str(singer_schema) + "\n" + str_records
        stream_file.write(str_stream)


def emit_message(singer_records: List[str]) -> None:
    for record in singer_records:
        print(record)


def main() -> None:
    # Entry Point
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--auth', action='store',
                        help='config file containing mixpanel credentials')
    parser.add_argument('-c', '--conf', action='store',
                        help='file containing the table properties')
    args = parser.parse_args()
    auth_file = args.auth
    conf_file = args.conf
    credentials = read_properties(auth_file)
    credentials = config_completion(credentials)
    tables = read_properties(conf_file)['tables']

    formatted_data = []
    for table in tables:
        print(table, file=sys.stderr)
        interm_data = []
        interm_data = load_data(table, credentials)
        formatted_data += interm_data
    formatted_data = [handle_null(dct) for dct in formatted_data]
    formatted_data = new_formatted_data(formatted_data)
    dtypes = take_dtypes(formatted_data)
    records = generate_singer_records(formatted_data, dtypes)
    emit_message(records)


if __name__ == "__main__":
    main()
