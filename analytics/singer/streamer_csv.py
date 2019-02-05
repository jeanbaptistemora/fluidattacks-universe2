#!/usr/bin/env python3

"""Minimalistic yet complete Streamer for a CSV file."""

import csv
import json
import argparse


def stream_csv(csv_file_path: str) -> None:
    """Streams a CSV file to stdout."""
    with open(csv_file_path) as csv_file:
        for row in csv.DictReader(
                csv_file,
                delimiter=",",
                quoting=csv.QUOTE_NONNUMERIC):
            print(
                json.dumps(
                    {
                        "stream": csv_file_path,
                        "record": dict(row)
                    }))


def main():
    """Usual entry point."""
    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csv_file_path",
        help="CSV file path to stream")
    args = parser.parse_args()

    stream_csv(args.csv_file_path)


if __name__ == "__main__":
    main()
