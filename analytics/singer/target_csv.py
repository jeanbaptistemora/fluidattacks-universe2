#!/usr/bin/env python3

"""Minimalistic yet complete Singer target for a csv file."""

import io
import sys
import csv
import json


CSV_PARAMS = {
    "extrasaction": "ignore",
    "delimiter": ",",
    "quotechar": '"',
    "quoting": csv.QUOTE_NONNUMERIC
}


def persist_messages():
    """Persist messages received in stdin to a csv file."""
    seen = {}
    headers = {}

    for message in io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"):
        json_obj = json.loads(message)
        if json_obj["type"] == "SCHEMA":
            stream = json_obj["stream"]
            headers[stream] = json_obj["schema"]["properties"].keys()

            if seen.get(stream, False):
                continue

            seen[stream] = True
            with open(f"{stream}.csv", "w") as csvfile:
                writer = csv.DictWriter(csvfile, headers[stream], **CSV_PARAMS)
                # primary keys
                writer.writerow(
                    dict(zip(headers[stream], json_obj["key_properties"])))
                # field names
                writer.writerow(
                    {
                        f: f
                        for f in headers[stream]})
                # field types
                writer.writerow(
                    {
                        f: json.dumps(v)
                        for f, v in json_obj["schema"]["properties"].items()})

        elif json_obj["type"] == "RECORD":
            stream = json_obj["stream"]
            with open(f"{stream}.csv", "a") as csvfile:
                writer = csv.DictWriter(csvfile, headers[stream], **CSV_PARAMS)
                writer.writerow(json_obj["record"])


def main():
    """Usual entry point."""
    persist_messages()


if __name__ == "__main__":
    main()
