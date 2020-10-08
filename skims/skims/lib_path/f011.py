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
    resolve,
    in_process,
)

# Local libraries
from lib_path.common import (
    SHIELD,
)
from nvd.local import (
    query,
)
from parse_json import (
    blocking_loads as blocking_json_loads,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Platform,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    blocking_to_snippet,
)
from zone import (
    t,
)

# Constants
DependencyType = Tuple[frozendict, frozendict]

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


def _build_gradle(
    content: str,
    path: str,
    platform: Platform,
) -> Tuple[Vulnerability, ...]:

    def resolve_dependencies() -> Iterator[DependencyType]:
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

            yield (
                {'column': column, 'line': line_no, 'item': product},
                {'column': column, 'line': line_no, 'item': version},
            )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=platform,
    )


@CACHE_ETERNALLY
@SHIELD
async def build_gradle(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _build_gradle,
        content=content,
        path=path,
        platform=Platform.MAVEN,
    )


def _npm_package_json(
    content: str,
    path: str,
    platform: Platform,
) -> Tuple[Vulnerability, ...]:
    content_json = blocking_json_loads(content, default={})

    dependencies: Iterator[DependencyType] = (
        (product, version)
        for key in content_json
        if key['item'] == 'dependencies'
        for product, version in content_json[key].items()
    )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        path=path,
        platform=platform,
    )


@CACHE_ETERNALLY
@SHIELD
async def npm_package_json(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _npm_package_json,
        content=content,
        path=path,
        platform=Platform.NPM,
    )


def _npm_package_lock_json(
    content: str,
    path: str,
    platform: Platform,
) -> Tuple[Vulnerability, ...]:

    def resolve_dependencies(obj: frozendict) -> Iterator[DependencyType]:
        for key in obj:
            if key['item'] in ('dependencies', 'devDependencies'):
                for product, spec in obj[key].items():
                    for spec_key, spec_val in spec.items():
                        if spec_key['item'] == 'version':
                            yield product, spec_val
                            yield from resolve_dependencies(spec)

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(
            obj=blocking_json_loads(content, default={}),
        ),
        path=path,
        platform=platform,
    )


@CACHE_ETERNALLY
@SHIELD
async def npm_package_lock_json(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _npm_package_lock_json,
        content=content,
        path=path,
        platform=Platform.NPM,
    )


def _yarn_lock(
    content: str,
    path: str,
    platform: Platform,
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

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=platform,
    )


@CACHE_ETERNALLY
@SHIELD
async def yarn_lock(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _yarn_lock,
        content=content,
        path=path,
        platform=Platform.NPM,
    )


def translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Iterator[DependencyType],
    path: str,
    platform: Platform,
) -> Tuple[Vulnerability, ...]:
    results: Tuple[Vulnerability, ...] = tuple(
        Vulnerability(
            finding=FindingEnum.F011,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=' '.join((
                path,
                f'({product["item"]} v{version["item"]})',
                f'[{cve}]',
            )),
            where=f'{product["line"]}',
            skims_metadata=SkimsVulnerabilityMetadata(
                cwe=('937',),
                description=t(
                    key='src.lib_path.f011.npm_package_json.description',
                    path=path,
                    product=product['item'],
                    version=version['item'],
                    cve=cve,
                ),
                snippet=blocking_to_snippet(
                    column=product['column'],
                    content=content,
                    line=product['line'],
                )
            )
        )
        for product, version in dependencies
        for cve in query(platform, product['item'], version['item'])
    )

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

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
