#!/usr/bin/env python3
"""Streamer for the Intercom API."""

import json
import argparse
import urllib.error
import urllib.request

from typing import List, Any

# type aliases for this module
JSON = Any


def request_resource(credentials: JSON, resource: str) -> JSON:
    """Request a resource and return a response."""
    request = urllib.request.Request(
        resource,
        headers={
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        })
    connection = urllib.request.urlopen(request)
    response_raw: str = connection.read().decode('utf-8')
    response_json: JSON = json.loads(response_raw)
    return response_json


def stream_it(name: str, json_obj: JSON) -> JSON:
    """Pack a JSON object to something that tap-JSON will understand."""
    packed_for_tap_json: JSON = {
        "stream": name,
        "record": json_obj
    }
    packed_for_tap_json_str: str = json.dumps(packed_for_tap_json)
    print(packed_for_tap_json_str)


def stream_iterable_endpoint(
        credentials: JSON,
        endpoint: str) -> None:
    """Stream to stdout a generic iterable endpoint."""
    page: int = 0

    resource: str = f"https://api.intercom.io/{endpoint}?per_page=50"
    response: JSON = {"pages": {"next": "true"}}

    while "pages" in response and response["pages"]["next"]:
        page += 1
        response = request_resource(credentials, f"{resource}&page={page}")
        for json_obj in response[endpoint]:
            stream_it(endpoint, json_obj)


def main():
    """Usual entry point."""
    endpoints: List[str] = [
        "users",
        "contacts",
        "companies",
        "admins",
        "teams",
        "segments",
        "conversations"
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--auth",
        help="JSON authentication file",
        dest="auth",
        type=argparse.FileType("r"),
        required=True)
    args = parser.parse_args()

    # load user credentials
    credentials = json.load(args.auth)

    # stream
    for endpoint in endpoints:
        stream_iterable_endpoint(credentials, endpoint)


if __name__ == "__main__":
    main()
