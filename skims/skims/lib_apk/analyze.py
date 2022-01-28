from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
from ctx import (
    CTX,
)
from lib_apk import (
    analyze_bytecodes,
)
from model import (
    core_model,
)
from more_itertools.more import (
    collapse,
)
from os import (
    cpu_count,
)
from parse_android_manifest import (
    get_apk_context,
    get_check_ctx as resolve_check_ctx,
)
from parse_android_manifest.types import (
    APKContext,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Set,
    Tuple,
)
from utils.fs import (
    resolve_paths,
)
from utils.function import (
    shield_blocking,
)

CHECKS: Tuple[
    Tuple[
        Callable[[APKContext], Any],
        Dict[
            core_model.FindingEnum,
            Callable[[Any], core_model.Vulnerabilities],
        ],
    ],
    ...,
] = ((resolve_check_ctx, analyze_bytecodes.CHECKS),)


@shield_blocking(on_error_return=[])
def analyze_one(
    apk_ctx: APKContext,
) -> Tuple[core_model.Vulnerability, ...]:
    return tuple(
        vulnerability
        for get_check_ctx, checks in CHECKS
        for finding, check in checks.items()
        if finding in CTX.config.checks and apk_ctx.apk_obj is not None
        for vulnerability in check(get_check_ctx(apk_ctx))
    )


def get_apk_contexts() -> Iterable[APKContext]:
    unique_paths, unique_nu_paths, unique_nv_paths = resolve_paths(
        exclude=CTX.config.apk.exclude,
        include=CTX.config.apk.include,
    )

    paths = list(unique_paths | unique_nu_paths | unique_nv_paths)
    for result in (get_apk_context(path) for path in paths):
        if result:
            yield result


def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(
        finding in CTX.config.checks
        for _, checks in CHECKS
        for finding in checks
    ):
        return

    unique_apk_contexts: Set[APKContext] = set(get_apk_contexts())
    vulnerabilities: Tuple[core_model.Vulnerability, ...] = tuple(
        collapse(
            (analyze_one(x) for x in unique_apk_contexts),
            base_type=core_model.Vulnerability,
        )
    )
    with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
        list(
            worker.map(
                lambda x: stores[  # pylint: disable=unnecessary-lambda
                    x.finding
                ].store(x),
                vulnerabilities,
            )
        )
