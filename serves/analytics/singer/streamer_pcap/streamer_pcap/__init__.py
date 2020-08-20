#!/usr/bin/env python3
"""Streamer for a Packet Capture (.pcap) file."""

import re
import json
import argparse
import datetime

from typing import Iterator, List, Any

import yaml
import scapy.all

# type aliases
JSON = Any
YAML = Any
PACKET = Any


def indent(level: int):
    """Return an indentation string."""
    return "  " * level


def date_from_timestamp(timestamp: float) -> str:
    """Return a RFC 3339 date from the timestamp."""
    date_obj = datetime.datetime.utcfromtimestamp(
        timestamp)
    date_str = date_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return date_str


def string_escape(string: str) -> str:
    """Escape a string to HEX.

    Packet data comes with not safe chars for YAML or JSON.
    They must be escaped and are recognized for beeing surrounded by ' or ".
    """
    # Return if not surrounded with ' or "
    if len(string) <= 2:
        return string
    for char in ("'", '"'):
        if string[0] == char and string[-1] == char:
            break
    else:
        return string

    new_string = ""
    reading_byte = 0
    for char in string[1:-2]:
        if reading_byte == 0:
            new_string += char.encode("ascii").hex().upper()
        elif reading_byte == 1 and char == "\\":
            reading_byte = 2
        elif reading_byte == 2 and char == "x":
            reading_byte = 3
        elif reading_byte == 3:
            reading_byte = 0
            new_string += char.upper()
    return new_string


def stream_it(name: str, json_obj: JSON) -> JSON:
    """Pack a JSON object to something that tap-JSON will understand."""
    packed_for_tap_json: JSON = {
        "stream": name,
        "record": json_obj
    }
    packed_for_tap_json_str: str = json.dumps(packed_for_tap_json)
    print(packed_for_tap_json_str)


def stream_packets(
        file_path: str,
        kwargs_list: List[str]) -> None:
    """Dump to JSON the pcap."""
    packets = scapy.all.rdpcap(file_path)
    for packet_object in packets:
        packet_encoded = stream_packets__encode(packet_object, kwargs_list)
        stream_it("packets", packet_encoded)


def stream_packets__encode( # noqa
        packet: PACKET,
        kwargs_list: List[str]) -> str:
    """Encode a packet object into a JSON."""
    # Control flow
    level: int = 0
    level_flag: int = 1
    level_level_flag: int = 1
    reading_list: bool = False
    reading_list_list: bool = False

    # Packet model
    packet_document: YAML = ""
    packet_iterlines: Iterator[str] = iter(
        packet.show2(dump=True).splitlines())

    # Packet parsing regexps
    re_base_header = re.compile(r"^###\[(.*)\]###$")
    re_base_body = re.compile(r"^([^=]*)=(.*)$")
    re_list_header = re.compile(r"^\|###\[(.*)\]###$")
    re_list_flag = re.compile(r"^\\(.*)\\$")
    re_list_body = re.compile(r"^\|([^=]*)=(.*)$")
    re_list_list_header = re.compile(r"^\|\|###\[(.*)\]###$")
    re_list_list_flag = re.compile(r"^\|\\(.*)\\$")
    re_list_list_body = re.compile(r"^\|\|([^=]*)=(.*)$")

    for key_val in kwargs_list:
        key, val = key_val.split("=", 1)
        packet_document += f'{key}: {val}\n'

    packet_document += f'packet_time: "{date_from_timestamp(packet.time)}"'

    try:
        while True:
            statement = stream_packets__encode__get(packet_iterlines)
            packet_document += "\n"

            # List List flag
            match = re_list_list_flag.match(statement)
            if match:
                if not reading_list_list:
                    level_level_flag = level
                    reading_list_list = True
                else:
                    level = level_level_flag
                packet_document += f"{indent(level+1)}{match.groups()[0]}:"
                continue

            # List List header
            match = re_list_list_header.match(statement)
            if match:
                packet_document += f"{indent(level+2)}- {match.groups()[0]}:"
                continue

            # List List body
            match = re_list_list_body.match(statement)
            if match:
                key, val = match.groups()
                val = string_escape(val)
                packet_document += f"{indent(level+4)}{key}: {val}"
                continue

            # List flag
            match = re_list_flag.match(statement)
            if match:
                if not reading_list:
                    level_flag = level
                    reading_list = True
                else:
                    level = level_flag
                packet_document += f"{indent(level+1)}{match.groups()[0]}:"
                continue

            # List header
            match = re_list_header.match(statement)
            if match:
                packet_document += f"{indent(level+2)}- {match.groups()[0]}:"
                continue

            # List body
            match = re_list_body.match(statement)
            if match:
                key, val = match.groups()
                val = string_escape(val)
                packet_document += f"{indent(level+4)}{key}: {val}"
                continue

            # Base header
            match = re_base_header.match(statement)
            if match:
                level = 0
                level_flag = 1
                packet_document += f"{indent(level)}{match.groups()[0]}:"
                reading_list = False
                continue

            # Base body
            match = re_base_body.match(statement)
            if match:
                key, val = match.groups()
                val = string_escape(val)
                packet_document += f"{indent(level+1)}{key}: {val}"
                reading_list = False
                continue
    except StopIteration:
        pass
    return yaml.load(packet_document)


def stream_packets__encode__get(
        packet_iterlines: Iterator[str]) -> str:
    """Return a formated statement from the iterable."""
    char_last: str = ""
    statement: str = ""
    inside_single_quote: bool = False
    for char in next(packet_iterlines):
        if char_last != "\\":
            if char == "'":
                inside_single_quote = not inside_single_quote
        if not inside_single_quote and char in (" ",):
            continue
        statement += char
        char_last = char
    return statement


def main():
    """Usual entry point."""
    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        help="Packet Capture file.")
    parser.add_argument(
        "--kwarg",
        action='append',
        help="Aditional metadata to append on every packet.",
        dest="kwargs_list")
    args = parser.parse_args()

    # stream the packets in the pcap file
    stream_packets(args.file, args.kwargs_list)


if __name__ == "__main__":
    main()
