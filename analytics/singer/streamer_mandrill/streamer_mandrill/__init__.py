""" Codegolf: Mandrill's API streamer
"""

import json
import argparse

import mandrill # pylint: disable=import-error

# packs a JSON object to something that tap-json will understand
PACK = lambda name, json_obj: {"stream": name, "record": json_obj}

# prints each json element from an iterable to stdout separated by 'sep'
SPRINT = lambda it: print(*(json.dumps(i) for i in it), sep="\n")

# streams to stdout a list of single JSON objects
STREAM_LIST = lambda name, list_obj: SPRINT(tuple(map(lambda x: PACK(name, x), list_obj)))

def main():
    """ usual entry point """

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
    STREAM_LIST("users", [worker.users.info()])
    # Search recently sent messages
    STREAM_LIST("messages", worker.messages.search())
    # Return all of the user-defined tag information
    STREAM_LIST("tags", worker.tags.list())
    # Retrieves your email rejection blacklist. Returns up to 1000 results.
    STREAM_LIST("blacklist", worker.rejects.list(include_expired=False))
    # Retrieves your email rejection whitelist. Returns up to 1000 results.
    STREAM_LIST("whitelist", worker.whitelists.list())
    # Return the senders that have tried to use this account.
    STREAM_LIST("senders", worker.senders.list())
    # Return a list of all the templates available to this user
    STREAM_LIST("templates", worker.templates.list())
    # Get the list of all webhooks defined on the account
    STREAM_LIST("webhooks", worker.webhooks.list())
    # Get the list of subaccounts defined for the account
    STREAM_LIST("subaccounts", worker.subaccounts.list())
    # List the domains that have been configured for inbound delivery
    STREAM_LIST("inbound", worker.inbound.domains())
    # Returns a list of your exports.
    STREAM_LIST("exports", worker.exports.list())
    # Lists your dedicated IPs.
    STREAM_LIST("ips", worker.ips.list())
    # Get the list of custom metadata fields indexed for the account.
    STREAM_LIST("metadata", worker.metadata.list())

if __name__ == "__main__":
    main()
