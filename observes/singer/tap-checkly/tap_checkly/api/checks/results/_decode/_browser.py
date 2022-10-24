# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    JsonObj,
    Maybe,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from tap_checkly.api._utils import (
    ExtendedUnfolder,
    switch_maybe,
)
from tap_checkly.objs.result import (
    BrowserCheckResult,
    TraceSummary,
    WebVitalMetric,
    WebVitals,
)


def _decode_metric(raw: JsonObj) -> ResultE[WebVitalMetric]:
    unfolder = ExtendedUnfolder(raw)
    return unfolder.require_primitive("score", str).bind(
        lambda s: unfolder.require_float("value").map(
            lambda v: WebVitalMetric(s, v)
        )
    )


def _get_metric(
    unfolder: ExtendedUnfolder, key: str
) -> ResultE[Maybe[WebVitalMetric]]:
    return switch_maybe(
        unfolder.get(key).map(
            lambda j: Unfolder(j).to_json().alt(Exception).bind(_decode_metric)
        )
    )


def _decode_vitals(raw: JsonObj) -> ResultE[WebVitals]:
    unfolder = ExtendedUnfolder(raw)

    def _metric(key: str) -> ResultE[Maybe[WebVitalMetric]]:
        return _get_metric(unfolder, key)

    return _metric("CLS").bind(
        lambda _cls: _metric("FCP").bind(
            lambda fcp: _metric("LCP").bind(
                lambda lcp: _metric("TBT").bind(
                    lambda tbt: _metric("TTFB").map(
                        lambda ttfb: WebVitals(_cls, fcp, lcp, tbt, ttfb)
                    )
                )
            )
        )
    )


def _decode_summary(raw: JsonObj) -> ResultE[TraceSummary]:
    unfolder = ExtendedUnfolder(raw)
    return unfolder.require_primitive("consoleErrors", int).bind(
        lambda console: unfolder.require_primitive("networkErrors", int).bind(
            lambda network: unfolder.require_primitive(
                "documentErrors", int
            ).bind(
                lambda document: unfolder.require_primitive(
                    "userScriptErrors", int
                ).map(
                    lambda user_script: TraceSummary(
                        console, network, document, user_script
                    )
                )
            )
        )
    )
