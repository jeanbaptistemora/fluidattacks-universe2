# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
    Union,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)
from metaloaders.model import (
    Node,
)

# Local libraries
from aws.utils import (
    create_vulns,
)
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
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_ec2_instances,
    iter_s3_buckets,
    iterate_resources,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)


def _iter_ec2_volumes(template: Node) -> Iterator[Node]:
    yield from (props for _, _, props in iterate_resources(
        template,
        'AWS::EC2::Volume',
        exact=True,
    ))


def _instances_without_role_iter_vulns(
    instaces_iterator: Iterator[Union[Any,
                                      Node]]) -> Iterator[Union[Any, Node]]:
    for instance in instaces_iterator:
        if isinstance(instance, Node):
            if not instance.raw.get('IamInstanceProfile', None):
                yield instance


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
) -> Tuple[Vulnerability, ...]:
    return create_vulns(
        content=content,
        description_key=('utils.model.finding.enum.F055_AWS.'
                         'instances_without_profile'),
        finding=FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_instances_without_role_iter_vulns(
            instaces_iterator=iter_ec2_instances(template=template)),
    )


def _cfn_public_buckets(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return create_vulns(
        content=content,
        description_key='utils.model.finding.enum.F055_AWS.public_buckets',
        finding=FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_public_buckets_iterate_vulnerabilities(
            buckets_iterator=iter_s3_buckets(template=template)),
    )


def _cfn_unencrypted_volumes(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return create_vulns(
        content=content,
        description_key=('utils.model.finding.enum.'
                         'F055_AWS.unencrypted_volumes'),
        finding=FindingEnum.F055_AWS,
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
) -> Tuple[Vulnerability, ...]:
    return create_vulns(
        content=content,
        description_key=('utils.model.finding.enum.'
                         'F055_AWS.unencrypted_buckets'),
        finding=FindingEnum.F055_AWS,
        path=path,
        statements_iterator=(bucket for bucket in iter_s3_buckets(template)
                             if not bucket.raw.get('BucketEncryption', None)),
    )


def _terraform_unencrypted_buckets(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    return create_vulns(
        content=content,
        description_key=('utils.model.finding.enum.'
                         'F055_AWS.unencrypted_buckets'),
        finding=FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_unencrypted_buckets_iterate_vulnerabilities(
            buckets_iterator=terraform_iter_s3_buckets(model=model)
        ),
    )


def _terraform_public_buckets(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    return create_vulns(
        content=content,
        description_key='utils.model.finding.enum.F055_AWS.public_buckets',
        finding=FindingEnum.F055_AWS,
        path=path,
        statements_iterator=_public_buckets_iterate_vulnerabilities(
            buckets_iterator=terraform_iter_s3_buckets(model=model)),
    )


@CACHE_ETERNALLY
@SHIELD
async def cfn_public_buckets(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
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
async def cfn_instances_without_profile(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _cfn_instances_without_profile,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
async def cfn_unencrypted_buckets(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag W41 S3 Bucket should have encryption option set
    return await in_process(
        _cfn_unencrypted_buckets,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
async def cfn_unencrypted_volumes(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag W37 EBS Volume should specify a KmsKeyId value\
    # cloudconformity EBS-001 EBS Encrypted
    return await in_process(
        _cfn_unencrypted_volumes,
        content=content,
        path=path,
        template=template,
    )


@SHIELD
async def terraform_unencrypted_buckets(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag W41 S3 Bucket should have encryption option set
    return await in_process(
        _terraform_unencrypted_buckets,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def terraform_public_buckets(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag F14 S3 Bucket should not have a public read-write acl
    # cfn_nag W31 S3 Bucket likely should not have a public read acl
    return await in_process(
        _terraform_public_buckets,
        content=content,
        path=path,
        model=model,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

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

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
