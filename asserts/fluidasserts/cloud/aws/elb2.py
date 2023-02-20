"""AWS cloud checks for ``ELB v2``` (Elastic Load Balancing version 2)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from fluidasserts import (
    DAST,
    HIGH,
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


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_insecure_ssl_cipher(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if Listeners uses unsafe SSL cipher.

    https://www.cloudconformity.com/knowledge-base/aws/ELB/
    elb-insecure-ssl-ciphers.html#

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    acceptable = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="elbv2",
        func="describe_ssl_policies",
        param="SslPolicies",
        Names=["ELBSecurityPolicy-2016-08"],
        retry=retry,
    )

    acceptable_protos = acceptable[0].get("Ciphers", [])

    balancers = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="elbv2",
        func="describe_load_balancers",
        param="LoadBalancers",
        retry=retry,
    )

    msg_open: str = "ELB Load Balancers allows insecure SSL ciphers"
    msg_closed: str = "ELB Load Balancers does not allow insecure SSL ciphers"

    vulns, safes = [], []

    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer["LoadBalancerArn"]

            for listener in aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="elbv2",
                func="describe_listeners",
                param="Listeners",
                LoadBalancerArn=load_balancer_arn,
                retry=retry,
            ):
                if listener.get("SslPolicy", ""):
                    policy = aws.run_boto3_func(
                        key_id=key_id,
                        secret=secret,
                        boto3_client_kwargs={
                            "aws_session_token": session_token
                        },
                        service="elbv2",
                        func="describe_ssl_policies",
                        param="SslPolicies",
                        Names=[listener["SslPolicy"]],
                        retry=retry,
                    )

                    for cipher in policy[0]["Ciphers"]:
                        (
                            vulns if cipher not in acceptable_protos else safes
                        ).append(
                            (
                                f'{listener["LoadBalancerArn"]}/'
                                f'{cipher["Name"]}',
                                "cipher is unsafe",
                            )
                        )

    return _get_result_as_tuple(
        service="ELBv2",
        objects="Application Load Balancers version 2",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
