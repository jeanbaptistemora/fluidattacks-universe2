from fa_purity import (
    FrozenDict,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.result.transform import (
    all_ok,
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
from typing import (
    Tuple,
)


def _decode_metric(raw: JsonObj) -> ResultE[Maybe[WebVitalMetric]]:
    unfolder = ExtendedUnfolder(raw)
    _score = unfolder.optional(
        "score",
        lambda u: u.to_optional(lambda uu: uu.to_primitive(str)).alt(
            Exception
        ),
    ).map(lambda m: m.bind(lambda o: Maybe.from_optional(o)))
    _value = unfolder.optional(
        "value",
        lambda u: ExtendedUnfolder.to_optional(
            u.jval, lambda v: ExtendedUnfolder.to_float(v)
        ).alt(Exception),
    ).map(lambda m: m.bind(lambda o: Maybe.from_optional(o)))

    def _from_values(
        score: Maybe[str], value: Maybe[float]
    ) -> ResultE[Maybe[WebVitalMetric]]:
        if score.value_or(None) is None and value.value_or(None) is None:
            return Result.success(Maybe.empty(WebVitalMetric), Exception)
        return (
            score.bind(
                lambda s: value.map(
                    lambda v: Maybe.from_value(WebVitalMetric(s, v))
                )
            )
            .to_result()
            .alt(
                lambda _: ValueError(
                    "Only one of `score` or `value` attributes on `WebVitalMetric` is `None`"
                )
            )
            .alt(Exception)
        )

    return _score.bind(lambda s: _value.bind(lambda v: _from_values(s, v)))


def _get_metric(
    unfolder: ExtendedUnfolder, key: str
) -> ResultE[Maybe[WebVitalMetric]]:
    return switch_maybe(
        unfolder.get(key).map(
            lambda j: Unfolder(j).to_json().alt(Exception).bind(_decode_metric)
        )
    ).map(lambda m: m.bind(lambda x: x))


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


def _decode_pages(
    raw: FrozenList[JsonValue],
) -> ResultE[FrozenDict[str, WebVitals]]:
    def _decode(j: JsonObj) -> ResultE[Tuple[str, WebVitals]]:
        unfolder = ExtendedUnfolder(j)
        return unfolder.require_primitive("url", str).bind(
            lambda url: unfolder.require_json("webVitals")
            .bind(_decode_vitals)
            .map(lambda w: (url, w))
        )

    return all_ok(
        tuple(Unfolder(j).to_json().alt(Exception).bind(_decode) for j in raw)
    ).map(lambda x: FrozenDict(dict(x)))


def decode_browser_result(raw: JsonObj) -> ResultE[BrowserCheckResult]:
    unfolder = ExtendedUnfolder(raw)
    return unfolder.require_primitive("type", str).bind(
        lambda framework: unfolder.require(
            "errors", lambda u: u.to_list_of(str).alt(Exception)
        ).bind(
            lambda errors: unfolder.require(
                "runtimeVersion", lambda u: u.to_primitive(str).alt(Exception)
            ).bind(
                lambda runtime: unfolder.require(
                    "traceSummary",
                    lambda u: u.to_json().alt(Exception).bind(_decode_summary),
                ).bind(
                    lambda trace: unfolder.require(
                        "pages", lambda u: u.to_list().alt(Exception)
                    )
                    .bind(_decode_pages)
                    .map(
                        lambda pages: BrowserCheckResult(
                            framework, errors, runtime, trace, pages
                        )
                    )
                )
            )
        )
    )
