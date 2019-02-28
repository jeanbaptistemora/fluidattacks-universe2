#!/usr/bin/env python3
"""Singer tap for the Ring Central API."""

import json
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
    json_obj: JSON = rc_platform.get("/account/~/extension/~").json_dict()
    stream_single("user", json_obj)


def stream_call_log(rc_platform: RC_PLATFORM) -> None:
    """Stream to stdout the call log."""
    page: int
    resource: str
    calllogs: JSON

    page = 1
    resource = (
        "/account/~/extension/~/call-log"
        "?showBlocked=true"
        "&view=Detailed"
        "&perPage=100"
        "&showDeleted=true")
    calllogs = rc_platform.get(
        f"{resource}&page={page}").json_dict()["records"]
    while calllogs:
        page += 1
        stream_iterable("call_log", calllogs)
        calllogs = rc_platform.get(
            f"{resource}&page={page}").json_dict()["records"]


def stream_contacts(rc_platform: RC_PLATFORM) -> None:
    """Stream to stdout the contacts."""
    page: int
    resource: str
    contacts: JSON

    page = 1
    resource = (
        "/account/~/extension/~/address-book/contact"
        "?perPage=100")
    contacts = rc_platform.get(
        f"{resource}&page={page}").json_dict()["records"]
    while contacts:
        page += 1
        stream_iterable("contacts", contacts)
        contacts = rc_platform.get(
            f"{resource}&page={page}").json_dict()["records"]


def stream_sms(rc_platform: RC_PLATFORM) -> None:
    """Stream to stdout the sms."""
    page: int
    resource: str
    sms: JSON

    page = 1
    resource = (
        "/account/~/extension/~/message-store"
        "?perPage=100")
    sms = rc_platform.get(
        f"{resource}&page={page}").json_dict()["records"]
    while sms:
        page += 1
        stream_iterable("sms", sms)
        sms = rc_platform.get(
            f"{resource}&page={page}").json_dict()["records"]


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
