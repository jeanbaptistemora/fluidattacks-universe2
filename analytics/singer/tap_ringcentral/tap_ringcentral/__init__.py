#!/usr/bin/env python3
"""Singer tap for the Ring Central API."""

import json
import argparse

from typing import Any

import ringcentral

# Type aliases
RC_SDK = Any
RC_PLATFORM = Any
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


def main():
    """Usual entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--auth",
        help='JSON authentication file',
        dest='auth',
        type=argparse.FileType('r'),
        required=True)
    args = parser.parse_args()

    credentials = json.load(args.auth)
    get_platform(credentials)


if __name__ == "__main__":
    main()
