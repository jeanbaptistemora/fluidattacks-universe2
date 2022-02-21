from aws.model import (
    AWSCloudfrontDistribution,
    AWSCTrail,
    AWSElb,
    AWSElbV2,
    AWSS3Bucket,
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
    iter_cloudfront_distributions,
    iter_cloudtrail_trail,
    iter_elb2_load_balancers,
    iter_elb_load_balancers,
    iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_bucket_has_logging_conf_disabled_iterate_vulnerabilities(
    file_ext: str,
    buckets_iterator: Iterator[Node],
) -> Iterator[AWSS3Bucket]:
    for bucket in buckets_iterator:
        logging = bucket.inner.get("LoggingConfiguration")
        if not isinstance(logging, Node):
            yield AWSS3Bucket(
                column=bucket.start_column,
                data=bucket.data,
                line=get_line_by_extension(bucket.start_line, file_ext),
            )


def _cfn_elb_has_access_logging_disabled_iterate_vulnerabilities(
    file_ext: str,
    load_balancers_iterator: Iterator[Node],
) -> Iterator[Union[AWSElb, Node]]:
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


def _cfn_distribution_has_logging_disabled_iterate_vulnerabilities(
    file_ext: str,
    distributions_iterator: Iterator[Node],
) -> Iterator[AWSCloudfrontDistribution]:
    for dist in distributions_iterator:
        dist_config = dist.inner["DistributionConfig"]
        if isinstance(dist_config, Node):
            logging = dist_config.inner.get("Logging")
            if not isinstance(logging, Node):
                yield AWSCloudfrontDistribution(
                    column=dist_config.start_column,
                    data=dist_config.data,
                    line=get_line_by_extension(
                        dist_config.start_line, file_ext
                    ),
                )


def _cfn_trails_not_multiregion_iterate_vulnerabilities(
    file_ext: str,
    trails_iterator: Iterator[Node],
) -> Iterator[Union[AWSCTrail, Node]]:
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


def _cfn_elb2_has_access_logs_s3_disabled_iterate_vulnerabilities(
    file_ext: str,
    load_balancers_iterator: Iterator[Node],
) -> Iterator[Union[AWSElbV2, Node]]:
    for elb in load_balancers_iterator:
        attrs = elb.inner.get("LoadBalancerAttributes")
        if not isinstance(attrs, Node):
            yield AWSElbV2(
                column=elb.start_column,
                data=elb.data,
                line=get_line_by_extension(elb.start_line, file_ext),
            )
        else:
            key_vals = [
                attr
                for attr in attrs.data
                if attr.raw["Key"] == "access_logs.s3.enabled"
            ]
            if key_vals:
                key = key_vals[0]
                if key.raw["Value"] in FALSE_OPTIONS:
                    yield key.inner["Value"]
            else:
                yield AWSElbV2(
                    column=attrs.start_column,
                    data=attrs.data,
                    line=get_line_by_extension(attrs.start_line, file_ext),
                )


def cfn_bucket_has_logging_conf_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.bucket_has_logging_conf_disabled",
        iterator=get_cloud_iterator(
            _cfn_bucket_has_logging_conf_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                buckets_iterator=iter_s3_buckets(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_LOG_CONF_DISABLED,
    )


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


def cfn_cf_distribution_has_logging_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.has_logging_disabled",
        iterator=get_cloud_iterator(
            _cfn_distribution_has_logging_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                distributions_iterator=iter_cloudfront_distributions(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_CF_DISTR_LOG_DISABLED,
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


def cfn_elb2_has_access_logs_s3_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f400.elb2_has_access_logs_s3_disabled",
        iterator=get_cloud_iterator(
            _cfn_elb2_has_access_logs_s3_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                load_balancers_iterator=iter_elb2_load_balancers(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_ELB2_LOGS_S3_DISABLED,
    )
