#!/usr/bin/env python3

"""Minimalistic yet complete Streamer for continuous's toe files."""

import re
import csv
import json
import glob


def stream_lines_csv(subs: str, lines_csv_path: str) -> None:
    """Streams the lines.csv file to stdout."""
    with open(lines_csv_path) as csv_file:
        for row in csv.DictReader(csv_file):
            print(json.dumps({
                "stream": f'lines_{subs}',
                "record": dict(row)
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
