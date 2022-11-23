from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    pure_map,
)
from fa_singer_io.json_schema import (
    JSchemaFactory,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from fa_singer_io.singer.encoder import (
    EncodeItem,
    SingerEncoder,
)
from fa_singer_io.singer.schema.core import (
    Property,
)
from tap_checkly.objs import (
    CheckId,
    CheckResultId,
    IndexedObj,
)
from tap_checkly.objs.result import (
    BrowserCheckResult,
    WebVitals,
)
from tap_checkly.singer._core import (
    SingerStreams,
)
from tap_checkly.singer._encoder import (
    ObjEncoder,
)
from typing import (
    Dict,
    Tuple,
)

_str_type = JSchemaFactory.from_prim_type(str)
_int_type = JSchemaFactory.from_prim_type(int)
_opt_str = JSchemaFactory.opt_prim_type(str)
_opt_float = JSchemaFactory.opt_prim_type(float)
BrowserCheckResultObj = IndexedObj[
    Tuple[CheckId, CheckResultId], BrowserCheckResult
]


@dataclass(frozen=True)
class _PagesObj:
    value: Tuple[CheckId, CheckResultId, str, WebVitals]


def _pages_encoder_fx() -> SingerEncoder[_PagesObj]:
    _mapper: Dict[str, EncodeItem[_PagesObj]] = {
        "check_id": EncodeItem.new(
            lambda x: x.value[0].id_str,
            Property(_str_type, True, False),
            _PagesObj,
        ),
        "result_id": EncodeItem.new(
            lambda x: x.value[1].id_str,
            Property(_str_type, True, False),
            _PagesObj,
        ),
        "url": EncodeItem.new(
            lambda x: x.value[2],
            Property(_str_type, True, False),
            _PagesObj,
        ),
        "webvital_cls_score": EncodeItem.new(
            lambda x: x.value[3].CLS.map(lambda w: w.score).value_or(None),
            Property(_opt_str, True, False),
            _PagesObj,
        ),
        "webvital_cls_value": EncodeItem.new(
            lambda x: x.value[3].CLS.map(lambda w: w.value).value_or(None),
            Property(_opt_float, True, False),
            _PagesObj,
        ),
        "webvital_fcp_score": EncodeItem.new(
            lambda x: x.value[3].FCP.map(lambda w: w.score).value_or(None),
            Property(_opt_str, True, False),
            _PagesObj,
        ),
        "webvital_fcp_value": EncodeItem.new(
            lambda x: x.value[3].FCP.map(lambda w: w.value).value_or(None),
            Property(_opt_float, True, False),
            _PagesObj,
        ),
        "webvital_lcp_score": EncodeItem.new(
            lambda x: x.value[3].LCP.map(lambda w: w.score).value_or(None),
            Property(_opt_str, True, False),
            _PagesObj,
        ),
        "webvital_lcp_value": EncodeItem.new(
            lambda x: x.value[3].LCP.map(lambda w: w.value).value_or(None),
            Property(_opt_float, True, False),
            _PagesObj,
        ),
        "webvital_tbt_score": EncodeItem.new(
            lambda x: x.value[3].TBT.map(lambda w: w.score).value_or(None),
            Property(_opt_str, True, False),
            _PagesObj,
        ),
        "webvital_tbt_value": EncodeItem.new(
            lambda x: x.value[3].TBT.map(lambda w: w.value).value_or(None),
            Property(_opt_float, True, False),
            _PagesObj,
        ),
        "webvital_ttfb_score": EncodeItem.new(
            lambda x: x.value[3].TTFB.map(lambda w: w.score).value_or(None),
            Property(_opt_str, True, False),
            _PagesObj,
        ),
        "webvital_ttfb_value": EncodeItem.new(
            lambda x: x.value[3].TTFB.map(lambda w: w.value).value_or(None),
            Property(_opt_float, True, False),
            _PagesObj,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_results_browser_pages.value, freeze(_mapper)
    )


def _core_encoder_fx() -> SingerEncoder[BrowserCheckResultObj]:
    _mapper: Dict[str, EncodeItem[BrowserCheckResultObj]] = {
        "check_id": EncodeItem.new(
            lambda x: x.id_obj[0].id_str,
            Property(_str_type, True, False),
            BrowserCheckResultObj,
        ),
        "result_id": EncodeItem.new(
            lambda x: x.id_obj[1].id_str,
            Property(_str_type, True, False),
            BrowserCheckResultObj,
        ),
        "framework": EncodeItem.new(
            lambda x: x.obj.framework,
            Property(_str_type, False, False),
            BrowserCheckResultObj,
        ),
        "runtime_ver": EncodeItem.new(
            lambda x: x.obj.runtime_ver,
            Property(_str_type, False, False),
            BrowserCheckResultObj,
        ),
        "summary_console_errors": EncodeItem.new(
            lambda x: x.obj.summary.console_errors,
            Property(_int_type, False, False),
            BrowserCheckResultObj,
        ),
        "summary_network_errors": EncodeItem.new(
            lambda x: x.obj.summary.network_errors,
            Property(_int_type, False, False),
            BrowserCheckResultObj,
        ),
        "summary_document_errors": EncodeItem.new(
            lambda x: x.obj.summary.document_errors,
            Property(_int_type, False, False),
            BrowserCheckResultObj,
        ),
        "summary_user_script_errors": EncodeItem.new(
            lambda x: x.obj.summary.user_script_errors,
            Property(_int_type, False, False),
            BrowserCheckResultObj,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_results_browser.value, freeze(_mapper)
    )


_pages_encoder = _pages_encoder_fx()
_core_encoder = _core_encoder_fx()


def _to_page(item: BrowserCheckResultObj) -> PureIter[_PagesObj]:
    return pure_map(
        lambda p: _PagesObj((item.id_obj[0], item.id_obj[1], p[0], p[1])),
        tuple(item.obj.pages.items()),
    )


def _to_records(item: BrowserCheckResultObj) -> PureIter[SingerRecord]:
    encoded_pages = _to_page(item).map(lambda p: _pages_encoder.record(p))
    items = (_core_encoder.record(item),) + tuple(encoded_pages)
    return from_flist(items)


_schemas = (_core_encoder.schema, _pages_encoder.schema)
encoder: ObjEncoder[BrowserCheckResultObj] = ObjEncoder.new(
    from_flist(_schemas),
    _to_records,
)
