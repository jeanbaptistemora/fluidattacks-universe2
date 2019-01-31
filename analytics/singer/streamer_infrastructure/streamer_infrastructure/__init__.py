"""Streamer for the Fluid Infrastructure."""

import json
import datetime
import argparse

from typing import Iterable, Dict, Any
import boto3 as amazon_sdk

# Type aliases that improve clarity
JSON = Any
SESSION = Any


class JSONEncoderOverrides(json.JSONEncoder):
    """Overrides to the JSON Encoder."""

    # pylint: disable=method-hidden, arguments-differ
    def default(self, obj):
        """Implement default overriders."""
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%SZ")
        return super(JSONEncoderOverrides, self).default(obj)


def jsonprint(obj: JSON) -> None:
    """Print to stdout a JSON object."""
    print(json.dumps(obj, cls=JSONEncoderOverrides, indent=2))


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
    # stream_redshift__describe_cluster_parameters(client)
    stream_redshift__describe_cluster_security_groups(client)
    # stream_redshift__describe_cluster_snapshots(client)
    stream_redshift__describe_cluster_subnet_groups(client)
    stream_redshift__describe_cluster_tracks(client)
    stream_redshift__describe_cluster_versions(client)
    stream_redshift__describe_clusters(client)
    # stream_redshift__describe_default_cluster_parameters(client)
    stream_redshift__describe_event_categories(client)
    stream_redshift__describe_event_subscriptions(client)
    # stream_redshift__describe_events(client)
    stream_redshift__describe_hsm_client_certificates(client)
    stream_redshift__describe_hsm_configurations(client)
    # stream_redshift__describe_logging_status(client)
    stream_redshift__describe_orderable_cluster_options(client)
    stream_redshift__describe_reserved_node_offerings(client)
    stream_redshift__describe_reserved_nodes(client)
    # stream_redshift__describe_resize(client)
    # stream_redshift__describe_snapshot_copy_grants(client)
    # stream_redshift__describe_snapshot_schedules(client)
    # stream_redshift__describe_storage(client)
    # stream_redshift__describe_table_restore_status(client)
    # stream_redshift__describe_tags(client)


def stream_redshift__describe_generic(
        func,
        table_name: str = "",
        response_key: str = "") -> None:
    """Streams a generic describe_*."""
    response = func()
    stream_iterable(table_name, response[response_key])
    while "Marker" in response:
        response = func(Marker=response["Marker"])
        stream_iterable(table_name, response[response_key])


def stream_redshift__describe_cluster_db_revisions(client):
    """Stream describe_cluster_db_revisions."""
    stream_redshift__describe_generic(
        client.describe_cluster_db_revisions,
        table_name="cluster_db_revisions",
        response_key="ClusterDbRevisions",
    )


def stream_redshift__describe_cluster_parameter_groups(client):
    """Stream describe_cluster_parameter_groups."""
    stream_redshift__describe_generic(
        client.describe_cluster_parameter_groups,
        table_name="cluster_parameter_groups",
        response_key="ParameterGroups",
    )


def stream_redshift__describe_cluster_security_groups(client):
    """Stream describe_cluster_security_groups."""
    stream_redshift__describe_generic(
        client.describe_cluster_security_groups,
        table_name="cluster_security_groups",
        response_key="ClusterSecurityGroups",
    )


def stream_redshift__describe_cluster_subnet_groups(client):
    """Stream describe_cluster_subnet_groups."""
    stream_redshift__describe_generic(
        client.describe_cluster_subnet_groups,
        table_name="cluster_subnet_groups",
        response_key="ClusterSubnetGroups",
    )


def stream_redshift__describe_cluster_tracks(client):
    """Stream describe_cluster_tracks."""
    stream_redshift__describe_generic(
        client.describe_cluster_tracks,
        table_name="cluster_tracks",
        response_key="MaintenanceTracks",
    )


def stream_redshift__describe_cluster_versions(client):
    """Stream describe_cluster_versions."""
    stream_redshift__describe_generic(
        client.describe_cluster_versions,
        table_name="cluster_versions",
        response_key="ClusterVersions",
    )


def stream_redshift__describe_clusters(client):
    """Stream describe_clusters."""
    stream_redshift__describe_generic(
        client.describe_clusters,
        table_name="clusters",
        response_key="Clusters",
    )


def stream_redshift__describe_event_categories(client):
    """Stream describe_event_categories."""
    stream_redshift__describe_generic(
        client.describe_event_categories,
        table_name="event_categories",
        response_key="EventCategoriesMapList",
    )


def stream_redshift__describe_event_subscriptions(client):
    """Stream describe_event_subscriptions."""
    stream_redshift__describe_generic(
        client.describe_event_subscriptions,
        table_name="event_subscriptions",
        response_key="EventSubscriptionsList",
    )


def stream_redshift__describe_hsm_client_certificates(client):
    """Stream describe_hsm_client_certificates."""
    stream_redshift__describe_generic(
        client.describe_hsm_client_certificates,
        table_name="hsm_client_certificates",
        response_key="HsmClientCertificates",
    )


def stream_redshift__describe_hsm_configurations(client):
    """Stream describe_hsm_configurations."""
    stream_redshift__describe_generic(
        client.describe_hsm_configurations,
        table_name="hsm_configurations",
        response_key="HsmConfigurations",
    )


def stream_redshift__describe_orderable_cluster_options(client):
    """Stream describe_orderable_cluster_options."""
    stream_redshift__describe_generic(
        client.describe_orderable_cluster_options,
        table_name="orderable_cluster_options",
        response_key="OrderableClusterOptions",
    )


def stream_redshift__describe_reserved_node_offerings(client):
    """Stream describe_reserved_node_offerings."""
    stream_redshift__describe_generic(
        client.describe_reserved_node_offerings,
        table_name="reserved_node_offerings",
        response_key="ReservedNodeOfferings",
    )


def stream_redshift__describe_reserved_nodes(client):
    """Stream describe_reserved_nodes."""
    stream_redshift__describe_generic(
        client.describe_reserved_nodes,
        table_name="reserved_nodes",
        response_key="ReservedNodes",
    )


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
