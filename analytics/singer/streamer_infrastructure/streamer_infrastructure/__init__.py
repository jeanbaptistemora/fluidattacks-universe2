"""Streamer for the Fluid Infrastructure."""

import json
import datetime
import argparse

from typing import Iterable, Dict, Any
import boto3 as amazon_sdk

# Type aliases that improve clarity
JSON = Any
SESSION = Any


class EncoderOverrides(json.JSONEncoder):
    """Overrides to the JSON Encoder."""

    # pylint: disable=method-hidden, arguments-differ
    def default(self, obj):
        """Implement default overriders."""
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%SZ")
        return super(EncoderOverrides, self).default(obj)


def jsonprint(obj: JSON) -> None:
    """Print to stdout a JSON object."""
    print(json.dumps(obj, cls=EncoderOverrides, indent=2))


def pack(name: str, json_obj: JSON) -> JSON:
    """Pack a JSON object to something that tap-json will understand."""
    return {"stream": name, "record": json_obj}


def stream_iterable(name: str, iterable: Iterable[JSON]) -> None:
    """Stream to stdout an iterable of single JSON objects."""
    for json_obj in iterable:
        jsonprint(pack(name, json_obj))


def get_connection(credentials: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    """Create an access point to the infrastructure."""
    session: SESSION = amazon_sdk.session.Session(
        aws_access_key_id=credentials["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=credentials["AWS_SECRET_ACCESS_KEY"],
        region_name=credentials["AWS_DEFAULT_REGION"]
    )

    connection = {
        "redshift": {
            "client": session.client('redshift'),
        }
    }

    return connection


def stream_redshift(client):
    """Stream JSON lines to stdout. with information about the service."""
    stream_redshift__describe_cluster_db_revisions(client)
    stream_redshift__describe_cluster_parameter_groups(client)
    stream_redshift__describe_cluster_parameter_groups(client)


def stream_redshift__describe_cluster_db_revisions(client):
    """Stream describe_cluster_db_revisions."""
    response = client.describe_cluster_db_revisions()
    stream_iterable(
        "cluster_db_revisions", response["ClusterDbRevisions"])
    while "Marker" in response:
        response = client.describe_cluster_db_revisions(
            Marker=response["Marker"])
        stream_iterable(
            "cluster_db_revisions", response["ClusterDbRevisions"])


def stream_redshift__describe_cluster_parameter_groups(client):
    """Stream describe_cluster_parameter_groups."""
    response = client.describe_cluster_parameter_groups()
    stream_iterable(
        "cluster_parameter_groups", response["ParameterGroups"])
    while "Marker" in response:
        response = client.describe_cluster_parameter_groups(
            Marker=response["Marker"])
        stream_iterable(
            "cluster_parameter_groups", response["ParameterGroups"])


def main():
    """Usual entry point."""
    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--auth',
        help='JSON authentication file',
        dest='auth',
        type=argparse.FileType('r'),
        required=True)
    args = parser.parse_args()

    credentials = json.load(args.auth)

    connection = get_connection(credentials)

    stream_redshift(connection["redshift"]["client"])


if __name__ == "__main__":
    main()
