# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
from contextlib import (
    suppress,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from metaloaders.model import (
    Node,
)

# Local libraries
from aws.model import (
    AWSS3Bucket,
    AWSS3Acl,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure import (
    iter_s3_buckets as terraform_iter_s3_buckets,
    get_argument,
    get_attribute,
)
from lib_path.common import (
    get_vulnerabilities_from_aws_iterator_blocking,
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_ec2_instances,
    iter_ec2_ingress_egress,
    iter_ec2_security_groups,
    iter_s3_buckets,
    iterate_resources,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.function import (
    TIMEOUT_1MIN,
)


def _iter_ec2_volumes(template: Node) -> Iterator[Node]:
    yield from (props for _, _, props in iterate_resources(
        template,
        'AWS::EC2::Volume',
        exact=True,
    ))


def _cidr_iter_vulnerabilities(
        rules_iterator: Iterator[Node]) -> Iterator[Node]:
    unrestricted_ipv4 = IPv4Network('0.0.0.0/0')
    unrestricted_ipv6 = IPv6Network('::/0')
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(AddressValueError, KeyError):
            if IPv4Network(
                    rule_raw['CidrIp'],
                    strict=False,
            ) == unrestricted_ipv4:
                yield rule.inner['CidrIp']
        with suppress(AddressValueError, KeyError):
            if IPv6Network(
                    rule_raw['CidrIpv6'],
                    strict=False,
            ) == unrestricted_ipv6:
                yield rule.inner['CidrIpv6']


def _instances_without_role_iter_vulns(
    instaces_iterator: Iterator[Union[Any,
                                      Node]]) -> Iterator[Union[Any, Node]]:
    for instance in instaces_iterator:
        if isinstance(instance, Node):
            if not instance.raw.get('IamInstanceProfile', None):
                yield instance


def _groups_without_egress_iter_vulnerabilities(
        groups_iterators: Iterator[Node]) -> Iterator[Node]:
    yield from (group for group in groups_iterators
                if not group.raw.get('SecurityGroupEgress', None))


def _unencrypted_volume_iterate_vulnerabilities(
    volumes_iterator: Iterator[Union[Any, Node]],
) -> Iterator[Union[Any, Node]]:
    for volume in volumes_iterator:
        if isinstance(volume, Node):
            if 'Encrypted' not in volume.raw:
                yield volume
            elif not volume.raw.get('Encrypted'):
                yield volume.inner['Encrypted']
            elif 'KmsKeyId' not in volume.raw:
                yield volume


def _public_buckets_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]]
) -> Iterator[Union[AWSS3Acl, Node]]:
    for bucket in buckets_iterator:
        if isinstance(bucket, Node):
            if bucket.raw.get('AccessControl', 'Private') == 'PublicReadWrite':
                yield bucket.inner['AccessControl']
        elif isinstance(bucket, AWSS3Bucket):
            acl = get_attribute(body=bucket.data, key='acl')
            if acl and acl.val == 'public-read-write':
                yield AWSS3Acl(
                    data=acl.val,
                    column=acl.column,
                    line=acl.line,
                )


def _unencrypted_buckets_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]]
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for bucket in buckets_iterator:
        if isinstance(bucket, Node):
            if not bucket.raw.get('BucketEncryption', None):
                yield bucket
        elif isinstance(bucket, AWSS3Bucket):
            if not get_argument(
                    key='server_side_encryption_configuration',
                    body=bucket.data,
            ):
                yield bucket


def _cfn_instances_without_profile(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key=('utils.model.finding.enum.F055_AWS.'
                         'instances_without_profile'),
        finding=core_model.FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_instances_without_role_iter_vulns(
            instaces_iterator=iter_ec2_instances(template=template)),
    )


def _cfn_public_buckets(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='utils.model.finding.enum.F055_AWS.public_buckets',
        finding=core_model.FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_public_buckets_iterate_vulnerabilities(
            buckets_iterator=iter_s3_buckets(template=template)),
    )


def _cfn_unencrypted_volumes(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key=('utils.model.finding.enum.'
                         'F055_AWS.unencrypted_volumes'),
        finding=core_model.FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_unencrypted_volume_iterate_vulnerabilities(
            volumes_iterator=_iter_ec2_volumes(
                template=template,
            )
        ),
    )


def _cfn_unencrypted_buckets(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key=('utils.model.finding.enum.'
                         'F055_AWS.unencrypted_buckets'),
        finding=core_model.FindingEnum.F055_AWS,
        path=path,
        statements_iterator=(bucket for bucket in iter_s3_buckets(template)
                             if not bucket.raw.get('BucketEncryption', None)),
    )


def _cfn_groups_without_egress(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f055_aws.security_group_without_egress',
        finding=core_model.FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_groups_without_egress_iter_vulnerabilities(
            groups_iterators=iter_ec2_security_groups(template=template)),
    )


def _cnf_unrestricted_cidrs(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f055_aws.unrestricted_cidrs',
        finding=core_model.FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_cidr_iter_vulnerabilities(
            rules_iterator=iter_ec2_ingress_egress(
                template=template,
                ingress=True,
                egress=True,
            )))


def _terraform_unencrypted_buckets(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key=('utils.model.finding.enum.'
                         'F055_AWS.unencrypted_buckets'),
        finding=core_model.FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_unencrypted_buckets_iterate_vulnerabilities(
            buckets_iterator=terraform_iter_s3_buckets(model=model)
        ),
    )


def _terraform_public_buckets(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='utils.model.finding.enum.F055_AWS.public_buckets',
        finding=core_model.FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_public_buckets_iterate_vulnerabilities(
            buckets_iterator=terraform_iter_s3_buckets(model=model)),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_groups_without_egress(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag F1000 Missing egress rule means all traffic is allowed outbound
    return await in_process(
        _cfn_groups_without_egress,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_public_buckets(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag F14 S3 Bucket should not have a public read-write acl
    # cfn_nag W31 S3 Bucket likely should not have a public read acl
    return await in_process(
        _cfn_public_buckets,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_instances_without_profile(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_instances_without_profile,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_unencrypted_buckets(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag W41 S3 Bucket should have encryption option set
    return await in_process(
        _cfn_unencrypted_buckets,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_unencrypted_volumes(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag W37 EBS Volume should specify a KmsKeyId value\
    # cloudconformity EBS-001 EBS Encrypted
    return await in_process(
        _cfn_unencrypted_volumes,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_unencrypted_buckets(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag W41 S3 Bucket should have encryption option set
    return await in_process(
        _terraform_unencrypted_buckets,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_public_buckets(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag F14 S3 Bucket should not have a public read-write acl
    # cfn_nag W31 S3 Bucket likely should not have a public read acl
    return await in_process(
        _terraform_public_buckets,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cnf_unrestricted_cidrs(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cnf_nag W2 Security Groups found with cidr open to world on ingress
    # cnf_nag W5 Security Groups found with cidr open to world on egress
    # cnf_nag W9 Security Groups found with ingress cidr that is not /32
    return await in_process(
        _cnf_unrestricted_cidrs,
        content=content,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(content=content,
                                             fmt=file_extension):
            coroutines.append(cfn_unencrypted_buckets(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cfn_unencrypted_volumes(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cfn_public_buckets(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cfn_instances_without_profile(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cnf_unrestricted_cidrs(
                content=content,
                path=path,
                template=template,
            ))
    elif file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(terraform_unencrypted_buckets(
            content=content,
            path=path,
            model=model,
        ))
        coroutines.append(terraform_public_buckets(
            content=content,
            path=path,
            model=model,
        ))

    return coroutines
