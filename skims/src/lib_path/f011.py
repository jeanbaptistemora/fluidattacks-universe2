# Standard library
import re
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Pattern,
    Tuple,
)

# Third party libraries
from frozendict import (
    frozendict,
)
from more_itertools import (
    windowed,
)

# Third party libraries
from aioextensions import (
    collect,
    resolve,
)

# Local libraries
from nvd.query import (
    get_vulnerabilities as get_nvd_vulnerabilities,
)
from parse_json import (
    loads as json_loads,
)
from state.ephemeral import (
    EphemeralStore,
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

NODE_JS_KEYWORDS: Tuple[str, ...] = ('node',)
NODE_JS_TARGET_SOFTWARE: str = 'node.js'
MAVEN_KEYWORDS: Tuple[str, ...] = ()
MAVEN_TARGET_SOFTWARE: str = ''

QUOTE = r'["\']'
TEXT = r'[^"\']+'
WS = r'\s*'

# Regexes
RE_MAVEN_A: Pattern[str] = re.compile(
    r'^.*'
    fr'{WS}(?:compile|implementation){WS}[(]?{WS}'
    fr'group{WS}:{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}'
    fr',{WS}name{WS}:{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}'
    fr'(?:,{WS}version{WS}:{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS})?'
    fr'.*$'
)
RE_MAVEN_B: Pattern[str] = re.compile(
    r'^.*'
    fr'{WS}(?:compile|implementation){WS}[(]?{WS}'
    fr'{QUOTE}(?P<statement>{TEXT}){QUOTE}'
    fr'.*$'
)

# Roadmap:
# | package           | weight | Implemented
# | build.gradle      | 3132   | yes
# | package.json      | 2823   | yes
# | packages.config   | 755    |
# | pom.xml           | 672    |
# | package-lock.json | 555    | yes
# | bower.json        | 158    |
# | yarn.lock         | 47     | yes


async def build_gradle(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    dependencies: List[DependencyType] = []

    for line_no, line in enumerate(content.splitlines(), start=1):
        if match := RE_MAVEN_A.match(line):
            column: int = match.start('group')
            product: str = match.group('group') + ':' + match.group('name')
            version: str = match.group('version') or '*'
        elif match := RE_MAVEN_B.match(line):
            column = match.start('statement')
            statement = match.group('statement')
            product, version = (
                statement.rsplit(':', maxsplit=1)
                if statement.count(':') >= 2
                else (statement, '*')
            )
        else:
            continue

        dependencies.append((
            {'column': column, 'line': line_no, 'item': product},
            {'column': column, 'line': line_no, 'item': version},
        ))

    return await translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=tuple(dependencies),
        keywords=MAVEN_KEYWORDS,
        path=path,
        target_software=MAVEN_TARGET_SOFTWARE,
    )


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

    return await translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        keywords=NODE_JS_KEYWORDS,
        path=path,
        target_software=NODE_JS_TARGET_SOFTWARE,
    )


async def npm_package_lock_json(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:

    def resolve_dependencies(
        obj: frozendict,
        current: List[DependencyType],
    ) -> List[DependencyType]:
        for key in obj:
            if key['item'] == 'dependencies':
                for product, spec in obj[key].items():
                    for spec_key, spec_val in spec.items():
                        if spec_key['item'] == 'version':
                            current.append((product, spec_val))
                            current = resolve_dependencies(spec, current)

        return current

    dependencies: Tuple[DependencyType, ...] = tuple(resolve_dependencies(
        await json_loads(content), [],
    ))

    return await translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        keywords=NODE_JS_KEYWORDS,
        path=path,
        target_software=NODE_JS_TARGET_SOFTWARE,
    )


async def yarn_lock(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:

    def resolve_dependencies() -> Iterator[DependencyType]:
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

    dependencies: Tuple[DependencyType, ...] = tuple(resolve_dependencies())

    return await translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        keywords=NODE_JS_KEYWORDS,
        path=path,
        target_software=NODE_JS_TARGET_SOFTWARE,
    )


async def translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Tuple[DependencyType, ...],
    keywords: Tuple[str, ...],
    path: str,
    target_software: str,
) -> Tuple[Vulnerability, ...]:
    query_results: Tuple[
        Tuple[DependencyType, Tuple[NVDVulnerability, ...]],
        ...
    ] = tuple(zip(
        dependencies,
        await collect((
            get_nvd_vulnerabilities(
                product=product['item'],
                version=version['item'],
                keywords=keywords,
                target_software=target_software,
            )
            for product, version in dependencies
        ), workers=5),
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
        if dependency_cve.code not in (
            'CVE-2017-12419',
            'CVE-2013-1779',
            'CVE-2012-5627',
            'CVE-2009-2942',
        )
    ])

    return results


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_name: str,
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if (file_name, file_extension) == ('build', 'gradle'):
        coroutines.append(build_gradle(
            content=await content_generator(),
            path=path,
        ))
    elif (file_name, file_extension) == ('package', 'json'):
        coroutines.append(npm_package_json(
            content=await content_generator(),
            path=path,
        ))
    elif (file_name, file_extension) == ('package-lock', 'json'):
        coroutines.append(npm_package_lock_json(
            content=await content_generator(),
            path=path,
        ))
    elif (file_name, file_extension) == ('yarn', 'lock'):
        coroutines.append(yarn_lock(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines):
        for result in await results:
            await store.store(result)
