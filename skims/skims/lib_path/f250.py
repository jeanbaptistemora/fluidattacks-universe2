from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEC2,
    AWSFSxFileSystem,
    AWSS3Bucket,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_ec2_volumes,
    iter_fsx_file_systems,
    iter_s3_buckets,
)
from parse_hcl2.common import (
    get_argument,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets as tfm_iter_s3_buckets,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from utils.function import (
    TIMEOUT_1MIN,
)

_FINDING_F250 = core_model.FindingEnum.F250
_FINDING_F250_CWE = _FINDING_F250.value.cwe


def _cfn_fsx_has_unencrypted_volumes_iter_vulns(
    file_ext: str,
    fsx_iterator: Iterator[Union[AWSFSxFileSystem, Node]],
) -> Iterator[Union[AWSFSxFileSystem, Node]]:
    for fsx in fsx_iterator:
        kms_key_id = fsx.inner.get("KmsKeyId")
        if not isinstance(kms_key_id, Node):
            yield AWSFSxFileSystem(
                column=fsx.start_column,
                data=fsx.data,
                line=get_line_by_extension(fsx.start_line, file_ext),
            )


def _tfm_unencrypted_buckets_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]]
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for bucket in buckets_iterator:
        if isinstance(bucket, Node):
            if not bucket.raw.get("BucketEncryption", None):
                yield bucket
        elif isinstance(bucket, AWSS3Bucket) and not get_argument(
            key="server_side_encryption_configuration",
            body=bucket.data,
        ):
            yield bucket


def _cfn_unencrypted_buckets_iterate_vulnerabilities(
    file_ext: str,
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]],
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for bucket in buckets_iterator:
        bck_encrypt = bucket.inner.get("BucketEncryption")
        if not isinstance(bck_encrypt, Node):
            yield AWSS3Bucket(
                column=bucket.start_column,
                data=bucket.data,
                line=get_line_by_extension(bucket.start_line, file_ext),
            )


def _cfn_ec2_has_unencrypted_volumes_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        if "Encrypted" not in ec2_res.raw:
            yield AWSEC2(
                column=ec2_res.start_column,
                data=ec2_res.data,
                line=get_line_by_extension(ec2_res.start_line, file_ext),
            )
        else:
            vol_encryption = ec2_res.inner.get("Encrypted")
            if vol_encryption.raw in FALSE_OPTIONS:
                yield vol_encryption
            elif "KmsKeyId" not in ec2_res.raw:
                yield AWSEC2(
                    column=ec2_res.start_column,
                    data=ec2_res.data,
                    line=get_line_by_extension(ec2_res.start_line, file_ext),
                )


def _cfn_fsx_has_unencrypted_volumes(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F250_CWE},
        description_key="src.lib_path.f250.fsx_has_unencrypted_volumes",
        finding=_FINDING_F250,
        iterator=get_cloud_iterator(
            _cfn_fsx_has_unencrypted_volumes_iter_vulns(
                file_ext=file_ext,
                fsx_iterator=iter_fsx_file_systems(template=template),
            )
        ),
        path=path,
    )


def _cfn_unencrypted_buckets(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F250_CWE},
        description_key="src.lib_path.f250.unencrypted_buckets",
        finding=_FINDING_F250,
        iterator=get_cloud_iterator(
            _cfn_unencrypted_buckets_iterate_vulnerabilities(
                file_ext=file_ext,
                buckets_iterator=iter_s3_buckets(template=template),
            )
        ),
        path=path,
    )


def _tfm_unencrypted_buckets(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F250_CWE},
        description_key="src.lib_path.f250.unencrypted_buckets",
        finding=_FINDING_F250,
        iterator=get_cloud_iterator(
            _tfm_unencrypted_buckets_iterate_vulnerabilities(
                buckets_iterator=tfm_iter_s3_buckets(model=model)
            )
        ),
        path=path,
    )


def _cfn_ec2_has_unencrypted_volumes(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F250_CWE},
        description_key="src.lib_path.f250.ec2_has_unencrypted_volumes",
        finding=_FINDING_F250,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unencrypted_volumes_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_volumes(template=template),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_fsx_has_unencrypted_volumes(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_fsx_has_unencrypted_volumes,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_unencrypted_buckets(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag W41 S3 Bucket should have encryption option set
    return await in_process(
        _cfn_unencrypted_buckets,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_unencrypted_buckets(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag W41 S3 Bucket should have encryption option set
    return await in_process(
        _tfm_unencrypted_buckets,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_unencrypted_volumes(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_unencrypted_volumes,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_fsx_has_unencrypted_volumes(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_unencrypted_buckets(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_ec2_has_unencrypted_volumes(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
    elif file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_unencrypted_buckets(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
