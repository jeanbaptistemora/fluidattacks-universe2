"""Streamer for the Fluid Infrastructure."""

import json
import datetime
import argparse

from typing import Iterable, List, Tuple, Set, Dict, Any

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
    print(json.dumps(obj, cls=JSONEncoderOverrides))


def pack(name: str, json_obj: JSON) -> JSON:
    """Pack a JSON object to something that tap-json will understand."""
    return {"stream": name, "record": json_obj}


def stream_iterable(name: str, iterable: Iterable[JSON]) -> None:
    """Stream to stdout an iterable of single JSON objects."""
    for json_obj in iterable:
        jsonprint(pack(name, json_obj))


def recover_key_from_iterable(
        list_obj: List[Any],
        iterable: Iterable[Any],
        keys: Any) -> None:
    """Append indexed elements from the iterable to list_obj."""
    if keys is not None:
        for json_obj in iterable:
            list_obj.append(tuple([json_obj[key] for key in keys if key]))


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
    # stream_redshift__describe_account_attributes(client)
    stream_redshift__describe_cluster_db_revisions(client)
    cluster_parameter_group_names, cluster_parameter_group_families = \
        stream_redshift__describe_cluster_parameter_groups(client)
    stream_redshift__describe_cluster_parameters(
        client, cluster_parameter_group_names)
    stream_redshift__describe_cluster_security_groups(client)
    stream_redshift__describe_cluster_snapshots(client)
    stream_redshift__describe_cluster_subnet_groups(client)
    stream_redshift__describe_cluster_tracks(client)
    stream_redshift__describe_cluster_versions(client)
    cluster_identifiers = stream_redshift__describe_clusters(client)
    stream_redshift__describe_default_cluster_parameters(
        client, cluster_parameter_group_families)
    stream_redshift__describe_event_categories(client)
    stream_redshift__describe_event_subscriptions(client)
    stream_redshift__describe_events(client)
    stream_redshift__describe_hsm_client_certificates(client)
    stream_redshift__describe_hsm_configurations(client)
    stream_redshift__describe_logging_status(client, cluster_identifiers)
    stream_redshift__describe_orderable_cluster_options(client)
    stream_redshift__describe_reserved_node_offerings(client)
    stream_redshift__describe_reserved_nodes(client)
    stream_redshift__describe_resize(client, cluster_identifiers)
    stream_redshift__describe_snapshot_copy_grants(client)
    stream_redshift__describe_snapshot_schedules(client)
    stream_redshift__describe_storage(client)
    stream_redshift__describe_table_restore_status(client, cluster_identifiers)
    stream_redshift__describe_tags(client)


def stream_redshift__describe_generic(
        func,
        table_name: str = "",
        response_key: str = "",
        recover_keys: Any = None,
        **kwargs) -> List[Any]:
    """Streams a generic describe_*."""
    returns: List[Any] = []
    response = func(**kwargs)
    stream_iterable(table_name, response[response_key])
    recover_key_from_iterable(
        returns, response[response_key], recover_keys)
    while "Marker" in response:
        response = func(Marker=response["Marker"], **kwargs)
        stream_iterable(table_name, response[response_key])
        recover_key_from_iterable(
            returns, response[response_key], recover_keys)
    return returns


def stream_redshift__describe_cluster_db_revisions(client):
    """Stream describe_cluster_db_revisions."""
    stream_redshift__describe_generic(
        client.describe_cluster_db_revisions,
        table_name="redshift_cluster_db_revisions",
        response_key="ClusterDbRevisions",
    )


def stream_redshift__describe_cluster_parameter_groups(
        client) -> Tuple[Set[str], Set[str]]:
    """Stream describe_cluster_parameter_groups."""
    returns = stream_redshift__describe_generic(
        client.describe_cluster_parameter_groups,
        table_name="redshift_cluster_parameter_groups",
        response_key="ParameterGroups",

        recover_keys=("ParameterGroupName", "ParameterGroupFamily",)
    )
    cluster_parameter_group_names = [i[0] for i in returns]
    cluster_parameter_group_families = [i[1] for i in returns]
    unique_r1 = set(cluster_parameter_group_names)
    unique_r2 = set(cluster_parameter_group_families)
    return unique_r1, unique_r2


def stream_redshift__describe_cluster_parameters(
        client,
        parameter_group_names) -> None:
    """Stream describe_cluster_parameters."""
    for parameter_group_name in parameter_group_names:
        stream_redshift__describe_generic(
            client.describe_cluster_parameters,
            table_name="redshift_cluster_parameters",
            response_key="Parameters",

            ParameterGroupName=parameter_group_name
        )


def stream_redshift__describe_cluster_security_groups(client):
    """Stream describe_cluster_security_groups."""
    stream_redshift__describe_generic(
        client.describe_cluster_security_groups,
        table_name="redshift_cluster_security_groups",
        response_key="ClusterSecurityGroups",
    )


def stream_redshift__describe_cluster_snapshots(client) -> None:
    """Stream describe_cluster_snapshots."""
    stream_redshift__describe_generic(
        client.describe_cluster_snapshots,
        table_name="redshift_cluster_snapshots",
        response_key="Snapshots",
    )


def stream_redshift__describe_cluster_subnet_groups(client):
    """Stream describe_cluster_subnet_groups."""
    stream_redshift__describe_generic(
        client.describe_cluster_subnet_groups,
        table_name="redshift_cluster_subnet_groups",
        response_key="ClusterSubnetGroups",
    )


def stream_redshift__describe_cluster_tracks(client):
    """Stream describe_cluster_tracks."""
    stream_redshift__describe_generic(
        client.describe_cluster_tracks,
        table_name="redshift_cluster_tracks",
        response_key="MaintenanceTracks",
    )


def stream_redshift__describe_cluster_versions(client):
    """Stream describe_cluster_versions."""
    stream_redshift__describe_generic(
        client.describe_cluster_versions,
        table_name="redshift_cluster_versions",
        response_key="ClusterVersions",
    )


def stream_redshift__describe_clusters(client) -> Set[str]:
    """Stream describe_clusters."""
    returns = stream_redshift__describe_generic(
        client.describe_clusters,
        table_name="redshift_clusters",
        response_key="Clusters",

        recover_keys=("ClusterIdentifier",)
    )
    cluster_identifiers = [i[0] for i in returns]
    return set(cluster_identifiers)


def stream_redshift__describe_default_cluster_parameters(
        client,
        cluster_parameter_group_families: Set[str]) -> None:
    """Stream describe_default_cluster_parameters."""
    for cluster_parameter_group_family in cluster_parameter_group_families:
        stream_redshift__describe_generic(
            client.describe_default_cluster_parameters,
            table_name="redshift_cluster_parameters",
            response_key="DefaultClusterParameters",

            ParameterGroupFamily=cluster_parameter_group_family
        )


def stream_redshift__describe_event_categories(client):
    """Stream describe_event_categories."""
    stream_redshift__describe_generic(
        client.describe_event_categories,
        table_name="redshift_event_categories",
        response_key="EventCategoriesMapList",
    )


def stream_redshift__describe_event_subscriptions(client):
    """Stream describe_event_subscriptions."""
    stream_redshift__describe_generic(
        client.describe_event_subscriptions,
        table_name="redshift_event_subscriptions",
        response_key="EventSubscriptionsList",
    )


def stream_redshift__describe_events(client):
    """Stream describe_events."""
    stream_redshift__describe_generic(
        client.describe_events,
        table_name="redshift_events",
        response_key="Events",

        # maximum last two weeks
        Duration=14 * 24 * 60
    )


def stream_redshift__describe_hsm_client_certificates(client):
    """Stream describe_hsm_client_certificates."""
    stream_redshift__describe_generic(
        client.describe_hsm_client_certificates,
        table_name="redshift_hsm_client_certificates",
        response_key="HsmClientCertificates",
    )


def stream_redshift__describe_hsm_configurations(client):
    """Stream describe_hsm_configurations."""
    stream_redshift__describe_generic(
        client.describe_hsm_configurations,
        table_name="redshift_hsm_configurations",
        response_key="HsmConfigurations",
    )


def stream_redshift__describe_logging_status(
        client,
        cluster_identifiers: Set[str]) -> None:
    """Stream describe_logging_status."""
    for cluster_identifier in cluster_identifiers:
        response = client.describe_logging_status(
            ClusterIdentifier=cluster_identifier)
        stream_iterable("redshift_logging_status", [response])
        while "Marker" in response:
            response = client.describe_logging_status(
                ClusterIdentifier=cluster_identifier,
                Marker=response["Marker"])
            stream_iterable("redshift_logging_status", [response])


def stream_redshift__describe_orderable_cluster_options(client):
    """Stream describe_orderable_cluster_options."""
    stream_redshift__describe_generic(
        client.describe_orderable_cluster_options,
        table_name="redshift_orderable_cluster_options",
        response_key="OrderableClusterOptions",
    )


def stream_redshift__describe_reserved_node_offerings(client):
    """Stream describe_reserved_node_offerings."""
    stream_redshift__describe_generic(
        client.describe_reserved_node_offerings,
        table_name="redshift_reserved_node_offerings",
        response_key="ReservedNodeOfferings",
    )


def stream_redshift__describe_reserved_nodes(client):
    """Stream describe_reserved_nodes."""
    stream_redshift__describe_generic(
        client.describe_reserved_nodes,
        table_name="redshift_reserved_nodes",
        response_key="ReservedNodes",
    )


def stream_redshift__describe_resize(
        client,
        cluster_identifiers: Set[str]) -> None:
    """Stream describe_resize."""
    for cluster_identifier in cluster_identifiers:
        try:
            response = client.describe_resize(
                ClusterIdentifier=cluster_identifier)
            stream_iterable("redshift_resize", [response])
            while "Marker" in response:
                response = client.describe_resize(
                    ClusterIdentifier=cluster_identifier,
                    Marker=response["Marker"])
                stream_iterable("redshift_resize", [response])
        except client.exceptions.ResizeNotFoundFault:
            pass


def stream_redshift__describe_snapshot_copy_grants(client) -> None:
    """Stream describe_snapshot_copy_grants."""
    stream_redshift__describe_generic(
        client.describe_snapshot_copy_grants,
        table_name="redshift_snapshot_copy_grants",
        response_key="SnapshotCopyGrants",
    )


def stream_redshift__describe_snapshot_schedules(client):
    """Stream describe_snapshot_schedules."""
    stream_redshift__describe_generic(
        client.describe_snapshot_schedules,
        table_name="redshift_snapshot_schedules",
        response_key="SnapshotSchedules",
    )


def stream_redshift__describe_storage(client):
    """Stream describe_storage."""
    response = client.describe_storage()
    stream_iterable("redshift_storage", (response,))


def stream_redshift__describe_table_restore_status(
        client,
        cluster_identifiers: Set[str]) -> None:
    """Stream describe_table_restore_status."""
    for cluster_identifier in cluster_identifiers:
        stream_redshift__describe_generic(
            client.describe_table_restore_status,
            table_name="redshift_table_restore_status",
            response_key="TableRestoreStatusDetails",

            ClusterIdentifier=cluster_identifier
        )


def stream_redshift__describe_tags(client):
    """Stream describe_tags."""
    stream_redshift__describe_generic(
        client.describe_tags,
        table_name="redshift_tags",
        response_key="TaggedResources",
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
