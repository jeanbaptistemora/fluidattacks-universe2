#!/usr/bin/env python3
"""Singer tap for the Ring Central API."""

import json
import time
import argparse

from typing import Iterable, Any

import ringcentral

# type aliases for ringcentral module
RC_SDK = Any
RC_PLATFORM = Any

# type aliases for this module
JSON = Any


def get_platform(credentials: JSON) -> RC_PLATFORM:
    """Return a platform interface to the API."""
    rc_sdk: RC_SDK = ringcentral.SDK(
        credentials["client_id"],
        credentials["client_secret"],
        credentials["client_server"])
    rc_platform: RC_PLATFORM = rc_sdk.platform()
    rc_platform.login(
        credentials["username"],
        credentials["extension"],
        credentials["password"])
    return rc_platform


def rc_platform__get(
        rc_platform: RC_PLATFORM,
        resource: str,
        api_group: str) -> JSON:
    """Query the RingCentral's platform without exceeding the rate limit."""
    minimum_time_between_requests: JSON = {
        "Auth": 12.0,
        "Heavy": 6.0,
        "Medium": 1.5,
        "Light": 1.2
    }
    time.sleep(minimum_time_between_requests.get(api_group, 12.0))
    return rc_platform.get(resource).json_dict()


def rc_platform__paginate_iterable(
        rc_platform: RC_PLATFORM,
        resource: str,
        api_name: str,
        api_group: str) -> None:
    """Paginates over an iterable API endpoint."""
    page: int = 1
    records: JSON = rc_platform__get(
        rc_platform, f"{resource}&page={page}", api_group)["records"]
    while records:
        page += 1
        stream_iterable(api_name, records)
        records = rc_platform__get(
            rc_platform, f"{resource}&page={page}", api_group)["records"]


def stream_it(name: str, json_obj: JSON) -> JSON:
    """Pack a JSON object to something that tap-JSON will understand."""
    packed_for_tap_json: JSON = {
        "stream": name,
        "record": json_obj
    }
    packed_for_tap_json_str: str = json.dumps(packed_for_tap_json)
    print(packed_for_tap_json_str)


def stream_single(name: str, json_obj: JSON) -> None:
    """Stream to stdout a single JSON obj."""
    stream_it(name, json_obj)


def stream_iterable(name: str, iterable: Iterable[JSON]) -> None:
    """Stream to stdout an iterable of single JSON objects."""
    for json_obj in iterable:
        stream_single(name, json_obj)


def stream_user(rc_platform: RC_PLATFORM) -> None:
    """Stream to stdout the user information."""
    json_obj: JSON = rc_platform__get(
        rc_platform, "/account/~/extension/~", "Heavy")
    stream_single("user", json_obj)


def stream_call_log(rc_platform: RC_PLATFORM) -> None:
    """Stream to stdout the call log."""
    resource = (
        "/account/~/extension/~/call-log"
        "?showBlocked=true"
        "&view=Detailed"
        "&perPage=100"
        "&showDeleted=true"
        "&dateFrom=1970-01-01T00:00:01Z")
    rc_platform__paginate_iterable(rc_platform, resource, "call_log", "Heavy")


def stream_contacts(rc_platform: RC_PLATFORM) -> None:
    """Stream to stdout the contacts."""
    resource = (
        "/account/~/extension/~/address-book/contact"
        "?perPage=100")
    rc_platform__paginate_iterable(rc_platform, resource, "contacts", "Heavy")


def stream_sms(rc_platform: RC_PLATFORM) -> None:
    """Stream to stdout the sms."""
    resource = (
        "/account/~/extension/~/message-store"
        "?perPage=100")
    rc_platform__paginate_iterable(rc_platform, resource, "sms", "Heavy")


def main():
    """Usual entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--auth",
        help="JSON authentication file",
        dest="auth",
        type=argparse.FileType("r"),
        required=True)
    for endpoint in ("user", "calls", "contacts", "sms"):
        parser.add_argument(
            f"--sync-{endpoint}",
            help=f"flag to indicate if {endpoint} data should be synced.",
            action=f"store_true",
            dest=f"do_sync_{endpoint}",
            default=False)
    args = parser.parse_args()

    # load user credentials
    credentials = json.load(args.auth)

    # get a platform access point
    rc_platform: RC_PLATFORM = get_platform(credentials)

    if args.do_sync_user:
        # stream /account/~/extension/~
        stream_user(rc_platform)
    if args.do_sync_calls:
        # stream /account/~/extension/~/call-log
        stream_call_log(rc_platform)
    if args.do_sync_contacts:
        # stream /account/~/extension/~/address-book/contact
        stream_contacts(rc_platform)
    if args.do_sync_sms:
        # stream /account/~/extension/~/message-store
        stream_sms(rc_platform)


if __name__ == "__main__":
    main()
