from collections.abc import (
    Callable,
    Coroutine,
)
from contextlib import (
    suppress,
)
from dast.aws.types import (
    Location,
)
from dast.aws.utils import (
    build_vulnerabilities,
    run_boto3_fun,
)
from model import (
    core_model,
)
from model.core_model import (
    AwsCredentials,
    Vulnerability,
)
from typing import (
    Any,
)


def _minimum_protoco_version(
    distribution_config: dict[Any, Any], distribution: dict[Any, Any]
) -> list[Location]:
    locations: list[Location] = []
    vulnerable_min_prot_versions = [
        "SSLv3",
        "TLSv1",
        "TLSv1_2016",
        "TLSv1.1_2016",
    ]
    with suppress(KeyError):
        min_prot_ver = distribution_config["ViewerCertificate"][
            "MinimumProtocolVersion"
        ]

        if min_prot_ver in vulnerable_min_prot_versions:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            "/ViewerCertificate/MinimumProtocolVersion",
                        ),
                        arn=(f"{distribution['ARN']}:"),
                        values=(min_prot_ver,),
                        description=(
                            "src.lib_path.f016"
                            ".serves_content_over_insecure_protocols"
                        ),
                    )
                ],
            ]
    return locations


def _origin_ssl_protocols(
    distribution_config: dict[Any, Any], distribution: dict[Any, Any]
) -> list[Location]:
    vulnerable_origin_ssl_protocols = ["SSLv3", "TLSv1", "TLSv1.1"]
    locations: list[Location] = []
    for index, origin in enumerate(distribution_config["Origins"]["Items"]):
        if custom_origin_config := origin.get("CustomOriginConfig", {}):
            for ssl_protocols in custom_origin_config["OriginSslProtocols"][
                "Items"
            ]:

                if ssl_protocols in vulnerable_origin_ssl_protocols:
                    locations = [
                        *locations,
                        *[
                            Location(
                                access_patterns=(
                                    (
                                        f"/Origins/Items/{index}"
                                        "/CustomOriginConfig"
                                        f"/OriginSslProtocols/Items"
                                    ),
                                ),
                                arn=(f"{distribution['ARN']}:"),
                                values=(ssl_protocols,),
                                description=(
                                    "src.lib_path.f016.serves_content_"
                                    "over_insecure_protocols"
                                ),
                            )
                        ],
                    ]
    return locations


async def serves_content_over_insecure_protocols(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudfront", function="list_distributions"
    )
    distribution_list = (
        response.get("DistributionList", []) if response else []
    )
    vulns: core_model.Vulnerabilities = ()
    if distribution_list:
        for distribution in distribution_list["Items"]:
            config: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="cloudfront",
                function="get_distribution",
                parameters={
                    "Id": str(distribution["Id"]),
                },
            )
            distribution_config = config["Distribution"]["DistributionConfig"]
            locations = _minimum_protoco_version(
                distribution_config, dict(distribution)
            )
            locations = [
                *locations,
                *_origin_ssl_protocols(
                    distribution_config, dict(distribution)
                ),
            ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_INSECURE_PROTOCOLS),
                    aws_response=distribution_config,
                ),
            )

    return vulns


async def elbv2_uses_insecure_ssl_protocol(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.AWS_ELBV2_INSECURE_PROTOCOLS
    vuln_protos = ["SSLv3", "TLSv1", "TLSv1.1"]
    describe_load_balancers: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="elbv2",
        function="describe_load_balancers",
    )
    balancers = (
        describe_load_balancers.get("LoadBalancers", [])
        if describe_load_balancers
        else []
    )
    vulns: core_model.Vulnerabilities = ()
    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer["LoadBalancerArn"]

            config: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="elbv2",
                function="describe_listeners",
                parameters={
                    "LoadBalancerArn": str(load_balancer_arn),
                },
            )
            locations: list[Location] = []
            listeners = config.get("Listeners", [])
            for listener in listeners:
                if listener.get("SslPolicy", ""):
                    describe_ssl_policies: dict[
                        str, Any
                    ] = await run_boto3_fun(
                        credentials,
                        service="elbv2",
                        function="describe_ssl_policies",
                        parameters={
                            "Names": [listener["SslPolicy"]],
                        },
                    )
                    policy = describe_ssl_policies.get("SslPolicies", [])
                    locations = [
                        Location(
                            access_patterns=("/0/SslProtocols",),
                            arn=(f"{listener['LoadBalancerArn']}"),
                            values=(protocol,),
                            description=(
                                "lib_path.f016."
                                "elbv2_uses_insecure_ssl_protocol"
                            ),
                        )
                        for protocol in policy[0]["SslProtocols"]
                        if protocol in vuln_protos
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=method,
                            aws_response=policy,
                        ),
                    )

    return vulns


async def elbv2_uses_insecure_ssl_cipher(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.AWS_ELBV2_INSECURE_SSL_CIPHER
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="elbv2",
        function="describe_ssl_policies",
        parameters={
            "Names": ["ELBSecurityPolicy-TLS-1-2-2017-01"],
        },
    )

    acceptable = response.get("SslPolicies", [])
    acceptable_protos = list(
        map(
            lambda item: item["Name"],
            acceptable[0].get("Ciphers", []) if acceptable else "",
        )
    )
    describe_load_balancers: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="elbv2",
        function="describe_load_balancers",
    )
    balancers = (
        describe_load_balancers.get("LoadBalancers", [])
        if describe_load_balancers
        else []
    )
    vulns: core_model.Vulnerabilities = ()
    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer["LoadBalancerArn"]

            config: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="elbv2",
                function="describe_listeners",
                parameters={
                    "LoadBalancerArn": str(load_balancer_arn),
                },
            )

            locations: list[Location] = []
            for listener in config.get("Listeners", []):
                if listener.get("SslPolicy", ""):
                    describe_ssl_policies: dict[
                        str, Any
                    ] = await run_boto3_fun(
                        credentials,
                        service="elbv2",
                        function="describe_ssl_policies",
                        parameters={
                            "Names": [listener["SslPolicy"]],
                        },
                    )
                    policy = describe_ssl_policies.get("SslPolicies", [])

                    locations = [
                        Location(
                            access_patterns=("/0/Ciphers",),
                            arn=(
                                f'{listener["LoadBalancerArn"]}/'
                                f'{cipher["Name"]}'
                            ),
                            values=(cipher["Name"],),
                            description=(
                                "lib_path.f016."
                                "elbv2_uses_insecure_ssl_protocol"
                            ),
                        )
                        for cipher in policy[0]["Ciphers"]
                        if cipher["Name"] not in acceptable_protos
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=method,
                            aws_response=policy,
                        ),
                    )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    serves_content_over_insecure_protocols,
    elbv2_uses_insecure_ssl_protocol,
    elbv2_uses_insecure_ssl_cipher,
)
