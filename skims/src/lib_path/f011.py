# Standard library
from itertools import (
    chain,
)
from typing import (
    AsyncGenerator,
    Awaitable,
    List,
    Tuple,
)

# Third party libraries
from frozendict import (
    frozendict,
)

# Local libraries
from nvd.query import (
    get_vulnerabilities as get_nvd_vulnerabilities,
)
from parse_json import (
    loads as json_loads,
)
from state import (
    cache_decorator,
)
from utils.aio import (
    materialize,
)
from utils.model import (
    FindingEnum,
    NVDVulnerability,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    to_snippet,
)
from zone import (
    t,
)

# Constants
DependencyType = Tuple[frozendict, frozendict]


@cache_decorator()
async def npm_package_json(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    obj = await json_loads(content)

    dependencies: Tuple[DependencyType, ...] = tuple(
        (product, version)
        for key in obj
        if key['item'] == 'dependencies'
        for product, version in obj[key].items()
    )

    query_results: Tuple[
        Tuple[DependencyType, Tuple[NVDVulnerability, ...]],
        ...
    ] = tuple(zip(
        dependencies,
        await materialize(
            get_nvd_vulnerabilities(
                product=product['item'],
                version=version['item'],
                keywords=('node',),
                target_software='node.js',
            )
            for product, version in dependencies
        ),
    ))

    results: Tuple[Vulnerability, ...] = tuple([
        Vulnerability(
            finding=FindingEnum.F011,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=' '.join((
                path,
                f'({dependency_cve.product} v{dependency_cve.version})',
                f'[{dependency_cve.code}]',
            )),
            where=f'{product["line"]}',
            skims_metadata=SkimsVulnerabilityMetadata(
                description=t(
                    key='src.lib_path.f011.npm_package_json.description',
                    path=path,
                    product=dependency_cve.product,
                    version=dependency_cve.version,
                    cve=dependency_cve.code,
                ),
                snippet=await to_snippet(
                    column=product['column'],
                    content=content,
                    line=product['line'],
                )
            )
        )
        for (product, version), dependency_cves in query_results
        for dependency_cve in dependency_cves
    ])

    return results


async def analyze(
    content_generator: AsyncGenerator[str, None],
    file_name: str,
    file_extension: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if (file_name, file_extension) == ('package', 'json'):
        coroutines.append(npm_package_json(
            content=await content_generator.__anext__(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await materialize(coroutines)
    ))

    return results
