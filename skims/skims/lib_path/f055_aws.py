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
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iterate_resources,
)
from parse_cfn.structure import (
    iter_s3_buckets
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
    buckets_iterator: Iterator[Union[Any,
                                     Node]], ) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        if isinstance(bucket, Node):
            if bucket.raw.get('AccessControl', 'Private') in (
                    'PublicRead',
                    'PublicReadWrite',
            ):
                yield bucket.inner['AccessControl']


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

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
