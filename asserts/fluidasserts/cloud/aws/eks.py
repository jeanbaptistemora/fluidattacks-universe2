# -*- coding: utf-8 -*-
"""AWS cloud checks (EKS)."""


# None


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from fluidasserts import (
    DAST,
    LOW,
    MEDIUM,
)
from fluidasserts.cloud.aws import (
    _get_result_as_tuple,
)
from fluidasserts.helper import (
    aws,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_endpoints_publicly_accessible(
    key_id: str,
    secret: str,
    session_token: str = None,
    retry: bool = True,
    client_kwargs: dict = None,
) -> tuple:
    """
    Check if the API servers of the Kubernetes cluster are publicly accessible.

    Disable public access to your API server endpoint so that it is not
    accessible from the Internet.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :param client_kwargs: boto3 client `kwargs <https://boto3.amazonaws.com/
      v1/documentation/api/latest/guide/session.html>`_.
    :returns: - ``OPEN`` if there is a public Kubernetes API server.
                accessible.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`

    """
    msg_open: str = (
        "The endpoints of the Kubernetes API server of the EKS"
        " clusters are publicly accessible from the Internet"
    )
    msg_closed: str = (
        "The endpoints of the Kubernetes API server of the EKS"
        " clusters are not publicly accessible from the Internet"
    )
    vulns, safes = [], []

    client_kwargs = client_kwargs or {}
    client_kwargs["aws_session_token"] = session_token

    clusters = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service="eks",
        func="list_clusters",
        param="clusters",
        boto3_client_kwargs=client_kwargs,
        retry=retry,
    )
    for cluster in clusters:
        cluster_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service="eks",
            func="describe_cluster",
            param="cluster",
            retry=retry,
            name=cluster,
            boto3_client_kwargs=client_kwargs,
        )
        vulnerable = (
            cluster_description["resourcesVpcConfig"]["endpointPrivateAccess"]
            is False
        ) and (
            cluster_description["resourcesVpcConfig"]["endpointPublicAccess"]
            is True
        )
        (vulns if vulnerable else safes).append(
            (
                cluster_description["arn"],
                (
                    "The API Server must not be publicly accessible, it should only"
                    " be accessible from an AWS Virtual Private Cloud (VPC)."
                ),
            )
        )

    return _get_result_as_tuple(
        service="EKS",
        objects="Clusters",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
