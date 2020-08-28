# Standard library
import re
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Literal,
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
from nvd.local import (
    query,
)
from parse_json import (
    loads as json_loads,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
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


def _get_build_gradle_dependencies(
    content: str,
) -> Tuple[DependencyType, ...]:
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

    return tuple(dependencies)


@cache_decorator()
async def build_gradle(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    dependencies: Tuple[DependencyType, ...] = await in_process(
        _get_build_gradle_dependencies,
        content=content,
    )

    return await translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        path=path,
        platform='MAVEN',
    )


def _get_npm_package_json_dependencies(
    content_json: Any,
) -> Tuple[DependencyType, ...]:
    dependencies: Tuple[DependencyType, ...] = tuple(
        (product, version)
        for key in content_json
        if key['item'] == 'dependencies'
        for product, version in content_json[key].items()
    )

    return dependencies


@cache_decorator()
async def npm_package_json(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    dependencies: Tuple[DependencyType, ...] = await in_process(
        _get_npm_package_json_dependencies,
        content_json=await json_loads(content, default={}),
    )

    return await translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        path=path,
        platform='NPM',
    )


def _get_npm_package_lock_json_dependencies(
    content_json: Any,
) -> Tuple[DependencyType, ...]:

    def resolve_dependencies(
        obj: frozendict,
        current: List[DependencyType],
    ) -> List[DependencyType]:
        for key in obj:
            if key['item'] in ('dependencies', 'devDependencies'):
                for product, spec in obj[key].items():
                    for spec_key, spec_val in spec.items():
                        if spec_key['item'] == 'version':
                            current.append((product, spec_val))
                            current = resolve_dependencies(spec, current)

        return current

    dependencies: Tuple[DependencyType, ...] = tuple(resolve_dependencies(
        content_json, [],
    ))

    return dependencies


@cache_decorator()
async def npm_package_lock_json(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    dependencies: Tuple[DependencyType, ...] = await in_process(
        _get_npm_package_lock_json_dependencies,
        content_json=await json_loads(content, default={}),
    )

    return await translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        path=path,
        platform='NPM',
    )


def _get_yarn_lock_dependencies(
    content: str,
) -> Tuple[DependencyType, ...]:

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

    return dependencies


@cache_decorator()
async def yarn_lock(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    dependencies: Tuple[DependencyType, ...] = await in_process(
        _get_yarn_lock_dependencies,
        content=content,
    )

    return await translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        path=path,
        platform='NPM',
    )


async def translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Tuple[DependencyType, ...],
    path: str,
    platform: Literal['NPM', 'MAVEN'],
) -> Tuple[Vulnerability, ...]:
    results: Tuple[Vulnerability, ...] = tuple([
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
                description=t(
                    key='src.lib_path.f011.npm_package_json.description',
                    path=path,
                    product=product['item'],
                    version=version['item'],
                    cve=cve,
                ),
                snippet=await to_snippet(
                    column=product['column'],
                    content=content,
                    line=product['line'],
                )
            )
        )
        for product, version in dependencies
        for cve in query(platform, product['item'], version['item'])
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

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
