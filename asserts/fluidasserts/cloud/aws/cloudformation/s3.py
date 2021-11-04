"""AWS CloudFormation checks for ``S3`` (Simple Storage Service)."""


from fluidasserts import (
    HIGH,
    LOW,
    MEDIUM,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_list_node_items,
    get_resources,
    get_templates,
    has_values,
    Vulnerability,
)
from fluidasserts.helper import (
    aws as helper,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from networkx import (
    DiGraph,
)
from typing import (
    List,
    Optional,
)

#: A set of available S3 Access Controls
ACCESS_CONTROLS = {
    "Private",
    "PublicRead",
    "PublicReadWrite",
    "AuthenticatedRead",
    "BucketOwnerRead",
    "BucketOwnerFullControl",
}


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_encryption_disabled(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any ``S3 Bucket`` has **Encryption** disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **BucketEncryption** attribute is not
                set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    buckets: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "S3", "Bucket"},
        num_labels=3,
        info=True,
    )
    for bucket, resource, template in buckets:
        _encryption: int = helper.get_index(
            get_resources(graph, bucket, "BucketEncryption", depth=4), 0
        )

        if not _encryption:
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=(f"AWS::S3::Bucket/" f"BucketEncryption/"),
                    identifier=resource["name"],
                    line=resource["line"],
                    reason="has encryption disabled.",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="S3 buckets have encryption disabled",
        msg_closed="S3 Buckets have encryption enabled",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_unauthorized_public_access(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if S3 buckets allow unauthorized public access via bucket policies.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if policies allow unauthorized public access.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    bucket_policies: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "S3", "BucketPolicy"},
        num_labels=3,
        info=True,
    )
    for bucket_policy, resource, template in bucket_policies:
        stmts = get_list_node_items(graph, bucket_policy, "Statement", depth=8)
        for stmt in stmts:
            vulnerable: List = has_values(
                graph, stmt, "Principal", ["*"], depth=12
            )
            if has_values(graph, stmt, "Effect", "Allow"):
                vulnerabilities.extend(
                    Vulnerability(
                        path=template["path"],
                        entity=(
                            f"AWS::S3::BucketPolicy/"
                            f"PolicyDocument/Statement/Principal"
                        ),
                        identifier=resource["name"],
                        line=graph.nodes.get(vuln)["line"],
                        reason="allows public access.",
                    )
                    for vuln in vulnerable
                )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="S3 bucket policy allows public access",
        msg_closed="S3 bucket policy allows public access",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_secure_transport(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if S3 buckets are protecting data in transit using SSL.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if policies allow insecure transport.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    bucket_policies: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "S3", "BucketPolicy"},
        num_labels=3,
        info=True,
    )
    for bucket_policy, resource, template in bucket_policies:
        vulnerable: List = []
        stmts = get_list_node_items(graph, bucket_policy, "Statement", depth=8)
        for stmt in stmts:
            yes_secure: List = has_values(
                graph,
                stmt,
                "SecureTransport",
                ["true", "True", True, "1", 1],
                depth=12,
            )
            no_secure: List = has_values(
                graph,
                stmt,
                "SecureTransport",
                ["false", "False", False, "0", 0],
                depth=12,
            )
            for item in yes_secure:
                if has_values(graph, stmt, "Effect", "Deny"):
                    vulnerable.append(item)
            for item in no_secure:
                if has_values(graph, stmt, "Effect", "Allow"):
                    vulnerable.append(item)
            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=(
                        f"AWS::S3::BucketPolicy/"
                        f"PolicyDocument/Statement/"
                        f"Condition/Bool/aws:SecureTransport"
                    ),
                    identifier=resource["name"],
                    line=graph.nodes.get(vuln)["line"],
                    reason="allows public access.",
                )
                for vuln in vulnerable
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="S3 bucket does not use SSL transport",
        msg_closed="S3 buckets use SSL transport",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_server_side_encryption_disabled(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if S3 buckets have Server-Side Encryption disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if policies disable server-side encryption.
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    bucket_policies: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "S3", "BucketPolicy"},
        num_labels=3,
        info=True,
    )
    for bucket_policy, resource, template in bucket_policies:
        vulnerable: List = []
        stmts = get_list_node_items(graph, bucket_policy, "Statement", depth=8)
        for stmt in stmts:
            sse: List = has_values(
                graph,
                stmt,
                "x-amz-server-side-encryption",
                ["false", "False", False, "0", 0],
                depth=19,
            )
            for item in sse:
                if has_values(graph, stmt, "Effect", "Allow"):
                    vulnerable.append(item)
        vulnerabilities.extend(
            Vulnerability(
                path=template["path"],
                entity=(
                    f"AWS::S3::BucketPolicy/"
                    f"PolicyDocument/Statement/"
                    f"Condition/Null/"
                    f"s3:x-amz-server-side-encryption"
                ),
                identifier=resource["name"],
                line=graph.nodes.get(vuln)["line"],
                reason="has serverside encryption disabled",
            )
            for vuln in vulnerable
        )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="S3 bucket policy allows unencrypted objects",
        msg_closed="S3 bucket policy does not allow unencrypted objects",
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_object_lock_disabled(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any ``S3 Bucket`` has **Object Lock** disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **ObjectLockConfiguration** attribute is not set or
    set to false.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    buckets: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "S3", "Bucket"},
        num_labels=3,
        info=True,
    )
    for bucket, resource, template in buckets:
        if not has_values(
            graph,
            bucket,
            "ObjectLockEnabled",
            ["true", "True", True, "1", 1],
            depth=5,
        ):
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=(f"AWS::S3::Bucket/" f"ObjectLockEnabled/"),
                    identifier=resource["name"],
                    line=resource["line"],
                    reason="has object lock disabled.",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="S3 buckets have object lock disabled",
        msg_closed="S3 Buckets have object lock enabled",
    )
