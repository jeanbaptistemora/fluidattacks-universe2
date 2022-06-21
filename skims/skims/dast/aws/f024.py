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
    Callable,
    Coroutine,
    Dict,
    List,
    Tuple,
)


def _port_in_open_seggroup(port: int, group: Dict[str, Any]) -> List[str]:
    vuln: List[str] = []
    for index, perm in enumerate(group["IpPermissions"]):
        with suppress(KeyError):
            if perm["FromPort"] <= port <= perm["ToPort"] and (
                (any(x["CidrIp"] == "0.0.0.0/0" for x in perm["IpRanges"]))
                or any(x["CidrIp"] == "::/0" for x in perm["Ipv6Ranges"])
            ):
                vuln = [*vuln, f"IpPermissions/{index}/ToPort"]
    return vuln


async def allows_anyone_to_admin_ports(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    admin_ports = {
        22,  # SSH
        1521,  # Oracle
        2438,  # Oracle
        3306,  # MySQL
        3389,  # RDP
        5432,  # Postgres
        6379,  # Redis
        7199,  # Cassandra
        8111,  # DAX
        8888,  # Cassandra
        9160,  # Cassandra
        11211,  # Memcached
        27017,  # MongoDB
        445,  # CIFS
    }

    security_groups: List[Dict[str, Any]] = (
        await run_boto3_fun(
            credentials, service="ec2", function="describe_security_groups"
        )
    ).get("SecurityGroups", [])

    locations = [
        Location(
            arn=(
                f"arn:aws:ec2::{group['OwnerId']}:"
                f"security-group/{group['GroupID']}"
            ),
            description=f"Must deny connections to port {port}",
            access_pattern=path,
            value=port,
        )
        for group in security_groups
        for port in admin_ports
        for path in _port_in_open_seggroup(port, group)
    ]
    return build_vulnerabilities(
        locations=locations,
        method=core_model.MethodsEnum.AWS_ANYONE_ADMIN_PORTS,
    )


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]]
] = (allows_anyone_to_admin_ports,)
