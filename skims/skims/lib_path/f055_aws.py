# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
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
async def cfn_unencrypted_buckets(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag S3 Bucket should have encryption option set
    return await in_process(
        _cfn_unencrypted_buckets,
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

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
