from aws.model import (
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
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
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
