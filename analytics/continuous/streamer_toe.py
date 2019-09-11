#!/usr/bin/env python3

"""Minimalistic yet complete Streamer for continuous's toe files."""

import re
import csv
import json
import glob
from datetime import datetime
from typing import Any, Callable, List, Tuple


def normalize_date(date_str: str) -> str:
    """Return a RFC 3339 date."""
    lines_format, rfc3339_format = '%Y-%m-%d', '%Y-%m-%dT%H:%M:%SZ'
    return datetime.strptime(date_str, lines_format).strftime(rfc3339_format)


def stream_lines_csv(subs: str, lines_csv_path: str) -> None:
    """Streams the lines.csv file to stdout."""
    lines_csv_fields: List[Tuple[str, Callable, Any]] = [
        # field_name, field_type, field_default_value
        ('filename', str, ''),
        ('comments', str, ''),
        ('modified-commit', str, ''),
        ('loc', int, 0),
        ('tested-lines', int, 0),
        ('modified-date', normalize_date, '2000-01-01'),
        ('tested-date', normalize_date, '2000-01-01'),
    ]

    with open(lines_csv_path) as csv_file:
        for row in csv.DictReader(csv_file):
            print(json.dumps({
                "stream": 'lines',
                "record": {
                    'subs': subs,
                    **{
                        field: function(row.get(field, default))
                        for field, function, default in lines_csv_fields
                    }
                }
            }))


def main():
    """Usual entry point."""
    lines_csv_glob: str = 'continuous/subscriptions/*/toe/lines.csv'
    for lines_csv_path in glob.glob(lines_csv_glob):
        subs, = re.match(pattern=r'continuous/subscriptions/(\w+)',
                         string=lines_csv_path).groups(1)
        stream_lines_csv(subs, lines_csv_path)


if __name__ == "__main__":
    main()
