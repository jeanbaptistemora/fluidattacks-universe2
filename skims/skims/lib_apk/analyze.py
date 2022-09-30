# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    List,
    Set,
    Tuple,
)
from utils.fs import (
    resolve_paths,
)
from utils.function import (
    shield_blocking,
)
from utils.logs import (
    log_blocking,
)

CHECKS: Tuple[
    Tuple[
        Callable[[APKContext], Any],
        Dict[
            core_model.FindingEnum,
            List[Callable[[Any], core_model.Vulnerabilities]],
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
        for finding, check_list in checks.items()
        if finding in CTX.config.checks and apk_ctx.apk_obj is not None
        for check in check_list
        for vulnerability in check(get_check_ctx(apk_ctx))
    )


def get_apk_contexts() -> Iterable[APKContext]:
    ok_paths, nu_paths, nv_paths = resolve_paths(
        include=CTX.config.apk.include,
        exclude=CTX.config.apk.exclude,
    )

    log_blocking("info", "Files to be tested: %s", len(ok_paths))

    all_paths = ok_paths + nu_paths + nv_paths
    for result in (get_apk_context(path) for path in all_paths):
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
