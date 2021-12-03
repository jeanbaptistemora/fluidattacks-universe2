"""AWS CloudFormation checks for ``ELB v2`` (Elastic Load Balancing v2)."""


from fluidasserts import (
    LOW,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_resources,
    get_templates,
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
    Set,
    Tuple,
)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_insecure_security_policy(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if Listeners uses unsafe security policy.

    https://www.cloudconformity.com/knowledge-base/aws/ELBv2/
    network-load-balancer-security-policy.html#

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if *SSLPolicy** attribute in the
                **Listener** is insecure.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    acceptable: Set = {
        "ELBSecurityPolicy-2016-08",
        "ELBSecurityPolicy-TLS-1-1-2017-01",
        "ELBSecurityPolicy-FS-2018-06",
        "ELBSecurityPolicy-TLS-1-2-Ext-2018-06",
    }
    vulnerabilities: list = []
    graph: DiGraph = get_graph(path, exclude)
    templates = get_templates(graph, path, exclude)
    listeners = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "ElasticLoadBalancingV2", "Listener"},
        info=True,
    )
    for listener, resource, template in listeners:
        policy_node = helper.get_index(
            get_resources(graph, listener, "SslPolicy", depth=3), 0
        )
        policy = graph.nodes[policy_node]["value"] if policy_node else ""
        if policy not in acceptable:
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=(
                        f"AWS::ElasticLoadBalancingV2::Listener" f"/{policy}"
                    ),
                    identifier=resource["name"],
                    line=graph.nodes[policy_node]["line"]
                    if policy_node
                    else graph.nodes[listener]["line"],
                    reason="is not secure",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="ELB Load Balancers implement insecure security policy",
        msg_closed=(
            "ELB Load Balancers do not implement " "insecure security policy"
        ),
    )
