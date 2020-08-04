# Standard library
from itertools import (
    chain,
)
from typing import (
    AsyncGenerator,
    Awaitable,
    Iterator,
    List,
    Tuple,
)

# Third party libraries
from frozendict import (
    frozendict,
)
from more_itertools import (
    windowed,
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

    return await npm(
        content=content,
        dependencies=dependencies,
        path=path,
    )


@cache_decorator()
async def npm_package_lock_json(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:

    def resolve(
        obj: frozendict,
        current: List[DependencyType],
    ) -> List[DependencyType]:
        for key in obj:
            if key['item'] == 'dependencies':
                for product, spec in obj[key].items():
                    for spec_key, spec_val in spec.items():
                        if spec_key['item'] == 'version':
                            current.append((product, spec_val))
                            current = resolve(spec, current)

        return current

    dependencies: Tuple[DependencyType, ...] = tuple(resolve(
        await json_loads(content), [],
    ))

    return await npm(
        content=content,
        dependencies=dependencies,
        path=path,
    )


@cache_decorator()
async def yarn_lock(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:

    def resolve() -> Iterator[DependencyType]:
        windower: Iterator[
            Tuple[Tuple[int, str], Tuple[int, str]],
        ] = windowed(  # type: ignore
            fillvalue='',
            n=2,
            seq=tuple(enumerate(content.splitlines(), start=1)),
            step=1,
        )

        # ((11479, 'zen-observable@^0.8.21:'), (11480, '  version "0.8.21"'))
        for (product_line, product), (version_line, version) in windower:
            product, version = product.strip(), version.strip()

            if (
                product.endswith(':') and not product.startswith(' ')
                and version.startswith('version')
            ):
                product = product.rstrip(':')
                product = product.split(',', maxsplit=1)[0]
                product = product.strip('"')
                product = product.rsplit('@', maxsplit=1)[0]

                version = version.split(' ', maxsplit=1)[1]
                version = version.strip('"')

                yield (
                    {'column': 0, 'line': product_line, 'item': product},
                    {'column': 0, 'line': version_line, 'item': version},
                )

    dependencies: Tuple[DependencyType, ...] = tuple(resolve())

    return await npm(
        content=content,
        dependencies=dependencies,
        path=path,
    )


async def npm(
    content: str,
    dependencies: Tuple[DependencyType, ...],
    path: str,
) -> Tuple[Vulnerability, ...]:
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
    elif (file_name, file_extension) == ('package-lock', 'json'):
        coroutines.append(npm_package_lock_json(
            content=await content_generator.__anext__(),
            path=path,
        ))
    elif (file_name, file_extension) == ('yarn', 'lock'):
        coroutines.append(yarn_lock(
            content=await content_generator.__anext__(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await materialize(coroutines)
    ))

    return results
