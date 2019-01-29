"""Streamer for the mandrill API.
"""

import json
import argparse

from typing import Iterable, List, Any

import mandrill

# Type aliases that improve clarity
JSON = Any


def pack(name: str, json_obj: JSON) -> JSON:
    """Packs a JSON object to something that tap-json will understand.
    """

    return {"stream": name, "record": json_obj}


def sprint(iterable: Iterable[Any]) -> None:
    """Prints each json element from an iterable to stdout separated by 'sep'.
    """

    print(*(json.dumps(i) for i in iterable), sep="\n")


def stream_list(name: str, list_obj: List[JSON]) -> None:
    """Streams to stdout a list of single JSON objects.
    """

    sprint(tuple(map(lambda x: pack(name, x), list_obj)))


def main():
    """Usual entry point.
    """

    parser = argparse.ArgumentParser(
        description="dumps calls to the mandrill API to a JSON stream")
    parser.add_argument(
        "-c", "--auth",
        required=True,
        type=argparse.FileType('r'),
        help="JSON authentication file, must contain 'api_key'")
    args = parser.parse_args()

    # Get authorization
    worker = mandrill.Mandrill(json.load(args.auth)["api_key"])

    # stream it ma'am!

    # Return the information about the API-connected user
    stream_list("users", [worker.users.info()])
    # Search recently sent messages
    stream_list("messages", worker.messages.search())
    # Return all of the user-defined tag information
    stream_list("tags", worker.tags.list())
    # Retrieves your email rejection blacklist. Returns up to 1000 results.
    stream_list("blacklist", worker.rejects.list(include_expired=False))
    # Retrieves your email rejection whitelist. Returns up to 1000 results.
    stream_list("whitelist", worker.whitelists.list())
    # Return the senders that have tried to use this account.
    stream_list("senders", worker.senders.list())
    # Return a list of all the templates available to this user
    stream_list("templates", worker.templates.list())
    # Get the list of all webhooks defined on the account
    stream_list("webhooks", worker.webhooks.list())
    # Get the list of subaccounts defined for the account
    stream_list("subaccounts", worker.subaccounts.list())
    # List the domains that have been configured for inbound delivery
    stream_list("inbound", worker.inbound.domains())
    # Returns a list of your exports.
    stream_list("exports", worker.exports.list())
    # Lists your dedicated IPs.
    stream_list("ips", worker.ips.list())
    # Get the list of custom metadata fields indexed for the account.
    stream_list("metadata", worker.metadata.list())


if __name__ == "__main__":
    main()
