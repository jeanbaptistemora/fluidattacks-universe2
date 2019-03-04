#!/usr/bin/env python3
"""Streamer for a Packet Capture (.pcap) file."""

import json
import argparse
import itertools

from typing import Any

import scapy.all

# type aliases
JSON = Any
PACKET = Any


def stream_it(name: str, json_obj: JSON) -> JSON:
    """Pack a JSON object to something that tap-JSON will understand."""
    packed_for_tap_json: JSON = {
        "stream": name,
        "record": json_obj
    }
    packed_for_tap_json_str: str = json.dumps(packed_for_tap_json)
    print(packed_for_tap_json_str)


def stream_packets(file: str) -> None:
    """Dump to JSON the pcap."""
    packets = scapy.all.rdpcap(file)
    for packet_object in packets:
        packet_encoded = stream_packets__encode(packet_object)
        stream_it("packets", packet_encoded)


def stream_packets__encode(packet: PACKET) -> str:
    """Encode a packet object into a JSON."""
    packet_object: JSON = {}
    packet_decoded = repr(packet)
    packet_decoded_iter = iter(packet_decoded)
    try:
        while True:
            name = stream_packets__encode__get_token(packet_decoded_iter)
            next(packet_decoded_iter)
            while True:
                packet_var = stream_packets__encode__get_token(
                    packet_decoded_iter)
                packet_val = stream_packets__encode__get_token(
                    packet_decoded_iter)
                packet_object[f"{name}__{packet_var}"] = packet_val
                packet_decoded_iter, copy = itertools.tee(packet_decoded_iter)
                if next(copy) == "|":
                    next(packet_decoded_iter)
                    break
    except StopIteration:
        pass
    return packet_object


def stream_packets__encode__get_token(packet_decoded_iter) -> str:
    """Get a token from the decoded packet."""
    token: str = ""
    last_char: str = ""
    reading_bracket: bool = False
    reading_quote: bool = False
    for char in packet_decoded_iter:
        if last_char != "\\":
            if char in ("'", "'"):
                reading_quote = not reading_quote
                continue
            if char in ("[", "]"):
                reading_bracket = not reading_bracket
                continue
            if char in ("<", ">"):
                continue
        if not reading_quote and not reading_bracket and char in (" ", "="):
            break
        last_char = char
        token += char
    return token


def main():
    """Usual entry point."""
    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        help="Packet Capture file.")
    args = parser.parse_args()

    stream_packets(args.file)


if __name__ == "__main__":
    main()
