from aws.model import (
    AWSCTrail,
    AWSEC2,
    AWSElb,
)
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
    TRUE_OPTIONS,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_cloudtrail_trail,
    iter_ec2_instances,
    iter_elb_load_balancers,
)
from typing import (
    Any,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_elb_has_access_logging_disabled_iterate_vulnerabilities(
    file_ext: str,
    load_balancers_iterator: Iterator[Node],
) -> Iterator[AWSElb | Node]:
    for elb in load_balancers_iterator:
        access_log = get_node_by_keys(elb, ["AccessLoggingPolicy", "Enabled"])
        if not isinstance(access_log, Node):
            yield AWSElb(
                column=elb.start_column,
                data=elb.data,
                line=get_line_by_extension(elb.start_line, file_ext),
            )
        elif access_log.raw in FALSE_OPTIONS:
            yield access_log


def _cfn_trails_not_multiregion_iterate_vulnerabilities(
    file_ext: str,
    trails_iterator: Iterator[Node],
) -> Iterator[AWSCTrail | Node]:
    for trail in trails_iterator:
        multi_reg = trail.inner.get("IsMultiRegionTrail")
        if not isinstance(multi_reg, Node):
            yield AWSCTrail(
                column=trail.start_column,
                data=trail.data,
                line=get_line_by_extension(trail.start_line, file_ext),
            )
        elif multi_reg.raw in FALSE_OPTIONS:
            yield multi_reg


def _cfn_ec2_monitoring_disabled_iterate_vulnerabilities(
    file_ext: str,
    res_iterator: Iterator[Node],
) -> Iterator[AWSEC2 | Node]:
    for res in res_iterator:
        monitoring = res.inner.get("Monitoring")
        if monitoring is None:
            yield AWSCTrail(  # type: ignore
                column=res.start_column,
                data=res.data,
                line=get_line_by_extension(res.start_line, file_ext),
            )
        elif hasattr(monitoring, "raw") and monitoring.raw not in TRUE_OPTIONS:
            yield monitoring


def cfn_elb_has_access_logging_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.elb_has_access_logging_disabled",
        iterator=get_cloud_iterator(
            _cfn_elb_has_access_logging_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                load_balancers_iterator=iter_elb_load_balancers(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_ELB_ACCESS_LOG_DISABLED,
    )


def cfn_trails_not_multiregion(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.trails_not_multiregion",
        iterator=get_cloud_iterator(
            _cfn_trails_not_multiregion_iterate_vulnerabilities(
                file_ext=file_ext,
                trails_iterator=iter_cloudtrail_trail(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_TRAILS_NOT_MULTIREGION,
    )


def cfn_ec2_monitoring_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.has_monitoring_disabled",
        iterator=get_cloud_iterator(
            _cfn_ec2_monitoring_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                res_iterator=iter_ec2_instances(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_EC2_MONITORING_DISABLED,
    )
